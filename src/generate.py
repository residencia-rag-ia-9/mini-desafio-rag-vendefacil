import re
from functools import lru_cache
from typing import Literal

from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from rank_bm25 import BM25Okapi

from config import OPENAI_API_KEY, OPENAI_MODEL
from src.retrieve import (
    hybrid_search,
    load_index,
    normalize,
    valid_values,
)
from src.schema import RAGResponse, SourceEvidence


# Dados que devem ser recusados
REFUSE = (
    "salario",
    "remuneracao",
    "cpf",
    "dados bancarios",
    "chave pix",
    "senha",
    "token",
    "credencial",
    "dados de saude",
)


# Saída simples que o LLM deve gerar
class Draft(BaseModel):
    answer: str

    confidence_level: Literal[
        "alta",
        "media",
        "baixa",
        "recusado",
    ]

    reasoning: str
    is_refusal: bool = False

    refusal_reason: Literal[
        "lgpd",
        "fora_de_escopo",
        "sem_evidencia",
    ] | None = None

    source_ids: list[int] = []


@lru_cache
def search_engine():
    """Carrega a busca uma única vez."""
    db = load_index()

    docs = list(
        db.docstore._dict.values()
    )

    bm25 = BM25Okapi([
        normalize(doc.page_content).split()
        for doc in docs
    ])

    return db, docs, bm25, valid_values(docs)


@lru_cache
def get_llm():
    """Carrega o LLM com saída estruturada."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY não configurada."
        )

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
    )

    return llm.with_structured_output(Draft)


def refusal(reason, message):
    """Cria uma recusa válida."""
    return RAGResponse(
        answer=message,
        confidence_level="recusado",
        sources_used=[],
        reasoning="Pergunta bloqueada pelo guardrail.",
        is_refusal=True,
        refusal_reason=reason,
    )


def lgpd_block(question):
    """Verifica dados que devem ser recusados."""
    text = normalize(question)

    return any(
        word in text
        for word in REFUSE
    )


def mask(text):
    """Ofusca dados pessoais."""
    # E-mail
    text = re.sub(
        r"[\w.+-]+@[\w.-]+\.\w+",
        "***@***",
        text,
    )

    # Telefone
    text = re.sub(
        r"\(?\d{2}\)?\s*9?\d{4,5}-?\d{4}",
        "(**) *****-****",
        text,
    )

    # Número de cartão
    text = re.sub(
        r"\b(?:\d[ -]*?){13,19}\b",
        "**** **** **** ****",
        text,
    )

    return text


def generate(question):
    """Executa o RAG completo."""

    # LGPD: recusa antes da busca
    if lgpd_block(question):
        return refusal(
            "lgpd",
            "Não posso fornecer esse dado por motivo de LGPD.",
        )

    db, docs, bm25, valid = search_engine()

    _, results = hybrid_search(
        db,
        bm25,
        docs,
        valid,
        question,
        use_filters=True,
    )

    if not results:
        return refusal(
            "sem_evidencia",
            "Não encontrei evidências para responder.",
        )

    # Mascara caso a pergunta envolva PII
    mask_data = any(
        word in normalize(question)
        for word in (
            "email",
            "e-mail",
            "telefone",
            "endereco",
            "cartao",
        )
    )

    context = []

    for i, doc in enumerate(results, 1):

        text = doc.page_content

        if mask_data:
            text = mask(text)

        context.append(
            f"[{i}] {doc.metadata['source_file']} "
            f"| {doc.metadata['chunk_id']}\n{text}"
        )

    prompt = f"""
Você é o assistente interno da VendeFácil.

Responda SOMENTE com base no contexto abaixo.

Se a pergunta não tiver relação com a VendeFácil:
is_refusal=true e refusal_reason=fora_de_escopo.

Se a pergunta for da empresa, mas não houver evidência:
is_refusal=true e refusal_reason=sem_evidencia.

Em source_ids informe os números das fontes
realmente usadas na resposta.

PERGUNTA:
{question}

CONTEXTO:
{chr(10).join(context)}
"""

    last_error = None

    # Retry obrigatório
    for _ in range(2):

        try:
            draft = get_llm().invoke(prompt)

            if draft.is_refusal:
                return refusal(
                    draft.refusal_reason or "sem_evidencia",
                    draft.answer,
                )

            selected = [
                results[i - 1]
                for i in draft.source_ids
                if 1 <= i <= len(results)
            ]

            if not selected:
                raise ValueError(
                    "LLM não informou uma fonte válida."
                )

            sources = []

            for doc in selected:

                quotation = doc.page_content[:500]

                if mask_data:
                    quotation = mask(quotation)

                sources.append(
                    SourceEvidence(
                        filepath=doc.metadata["source_file"],
                        chunk_id=doc.metadata["chunk_id"],
                        quotation=quotation,
                    )
                )

            confidence = draft.confidence_level

            if confidence == "recusado":
                confidence = "baixa"

            return RAGResponse(
                answer=mask(draft.answer)
                if mask_data
                else draft.answer,

                confidence_level=confidence,
                sources_used=sources,
                reasoning=draft.reasoning,
                is_refusal=False,
                refusal_reason=None,
            )

        except Exception as error:
            last_error = error

    return refusal(
        "sem_evidencia",
        f"Não foi possível validar a resposta: {last_error}",
    )


def main():
    question = input("Pergunta: ")

    response = generate(question)

    print(
        response.model_dump_json(
            indent=2
        )
    )


if __name__ == "__main__":
    main()