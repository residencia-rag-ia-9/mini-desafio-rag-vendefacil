import re
from functools import lru_cache
from typing import Literal

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
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
SENSITIVE_TERMS = (
    "cpf",
    "dados bancarios",
    "conta bancaria",
    "chave pix",
    "senha",
    "password",
    "token",
    "credencial",
    "chave de api",
    "api key",
    "dados de saude",
    "diagnostico",
    "prontuario",
    "doenca",
)

# Consultas de salário individual
SALARY_TERMS = (
    "salario atual",
    "salario individual",
    "salario de",
    "salario do",
    "salario da",
    "salarios de",
    "salarios do",
    "salarios da",
    "quanto ganha",
    "lista de salarios",
    "ordem de remuneracao",
    "remuneracao individual",
)

# Dados que devem ser mascarados
MASK_TERMS = (
    "email",
    "e-mail",
    "telefone",
    "celular",
    "endereco",
    "cartao",
)


class DraftEvidence(BaseModel):
    """Evidência escolhida pelo LLM."""

    source_id: int
    quotation: str = Field(max_length=500)


class Draft(BaseModel):
    """Resposta provisória do LLM."""

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

    evidences: list[DraftEvidence] = Field(
        default_factory=list
    )


@lru_cache
def search_engine():
    """Carrega FAISS e BM25 uma única vez."""

    db = load_index()

    documents = list(
        db.docstore._dict.values()
    )

    bm25 = BM25Okapi([
        normalize(doc.page_content).split()
        for doc in documents
    ])

    valid = valid_values(documents)

    return db, documents, bm25, valid


@lru_cache
def get_llm():
    """Configura o LLM com saída estruturada."""

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
    """Gera uma recusa válida."""

    return RAGResponse(
        answer=message,
        confidence_level="recusado",
        sources_used=[],
        reasoning="Pergunta bloqueada ou sem evidência suficiente.",
        is_refusal=True,
        refusal_reason=reason,
    )


def lgpd_block(question):
    """Detecta dados que devem ser recusados."""

    text = normalize(question)

    # Dados sensíveis
    if any(
        term in text
        for term in SENSITIVE_TERMS
    ):
        return True

    # Média salarial pode ser respondida
    if (
        "media salarial" in text
        or "salario medio" in text
    ):
        return False

    # Salário individual deve ser recusado
    if any(
        term in text
        for term in SALARY_TERMS
    ):
        return True

    return False


def needs_mask(question):
    """Detecta dados que devem ser mascarados."""

    text = normalize(question)

    return any(
        term in text
        for term in MASK_TERMS
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

    # Endereço
    text = re.sub(
        r"(?i)((?:endereco|address)(?: residencial)?\s*:\s*)"
        r"[^.\n]+",
        r"\1[OCULTO]",
        text,
    )

    # Cartão
    text = re.sub(
        r"\b(?:\d[ -]*?){13,19}\b",
        "**** **** **** ****",
        text,
    )

    return text


def generate(question):
    """Executa recuperação, guardrails e geração."""

    # LGPD: bloqueia antes da busca
    if lgpd_block(question):
        return refusal(
            "lgpd",
            "Não posso fornecer esse dado por motivo de LGPD.",
        )

    db, documents, bm25, valid = search_engine()

    _, results = hybrid_search(
        db,
        bm25,
        documents,
        valid,
        question,
        use_filters=True,
    )

    # Aqui realmente não existem evidências
    if not results:
        return refusal(
            "sem_evidencia",
            "Não encontrei evidências para responder.",
        )

    mask_data = needs_mask(question)

    context_docs = []

    for doc in results:

        content = doc.page_content

        if mask_data:
            content = mask(content)

        context_docs.append(content)

    context = "\n\n".join(
        (
            f"[{index}] "
            f"Arquivo: {doc.metadata['source_file']}\n"
            f"Chunk: {doc.metadata['chunk_id']}\n"
            f"Sensibilidade: "
            f"{doc.metadata.get('sensitivity', 'interno')}\n"
            f"Conteúdo:\n{context_docs[index - 1]}"
        )
        for index, doc in enumerate(results, 1)
    )

    prompt = f"""
Você é o assistente corporativo da VendeFácil.

Responda somente usando as fontes fornecidas.

REGRAS:

- Não use conhecimento externo.
- Se a pergunta não tiver relação com a VendeFácil,
  recuse com refusal_reason="fora_de_escopo".
- Se não houver evidência suficiente,
  recuse com refusal_reason="sem_evidencia".
- Uma resposta normal deve possuir evidência.
- Em cada evidência, source_id deve indicar a fonte usada.
- quotation deve ser copiada literalmente da fonte indicada.
- Não invente trechos.
- Use confidence_level alta, media ou baixa em respostas normais.
- Use recusado somente quando is_refusal=true.

PERGUNTA:
{question}

FONTES:
{context}
"""

    last_error = None

    # Duas tentativas em caso de falha
    for _ in range(2):

        try:

            draft = get_llm().invoke(prompt)

            if draft.is_refusal:
                return refusal(
                    draft.refusal_reason
                    or "sem_evidencia",
                    draft.answer,
                )

            if not draft.evidences:
                raise ValueError(
                    "Resposta sem evidência."
                )

            sources = []

            for evidence in draft.evidences:

                if not (
                    1 <= evidence.source_id <= len(results)
                ):
                    raise ValueError(
                        "ID de fonte inválido."
                    )

                doc = results[
                    evidence.source_id - 1
                ]

                content = doc.page_content

                if mask_data:
                    content = mask(content)

                quotation = evidence.quotation.strip()

                # O trecho precisa realmente existir
                if quotation not in content:
                    raise ValueError(
                        "Trecho citado não existe na fonte."
                    )

                sources.append(
                    SourceEvidence(
                        filepath=doc.metadata[
                            "source_file"
                        ],
                        chunk_id=doc.metadata[
                            "chunk_id"
                        ],
                        quotation=quotation,
                    )
                )

            confidence = draft.confidence_level

            if confidence == "recusado":
                confidence = "baixa"

            answer = draft.answer

            if mask_data:
                answer = mask(answer)

            return RAGResponse(
                answer=answer,
                confidence_level=confidence,
                sources_used=sources,
                reasoning=draft.reasoning,
                is_refusal=False,
                refusal_reason=None,
            )

        except Exception as error:
            last_error = error

    # Erro da API ou falha após as duas tentativas
    raise RuntimeError(
        f"Erro ao gerar resposta: {last_error}"
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