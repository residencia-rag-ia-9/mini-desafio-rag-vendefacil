from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL


class JudgeResult(BaseModel):
    correctness: float = Field(ge=0, le=1)
    answer_relevance: float = Field(ge=0, le=1)
    groundedness: float = Field(ge=0, le=1)


def evaluate_answer(question, answer, ground_truth, evidences):
    """Avalia a resposta do RAG usando um LLM."""

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
    ).with_structured_output(JudgeResult)

    evidence_text = "\n".join(evidences)

    prompt = f"""
Avalie a resposta de um sistema RAG da VendeFácil.

Dê notas entre 0 e 1.

Pergunta:
{question}

Resposta gerada:
{answer}

Resposta esperada:
{ground_truth}

Evidências:
{evidence_text}

Avalie:

correctness:
A resposta está correta em relação ao gabarito?

answer_relevance:
A resposta realmente responde à pergunta?

groundedness:
A resposta está sustentada pelas evidências?

Em caso de uma recusa correta por LGPD ou fora de escopo,
não penalize groundedness apenas pela ausência de citações.
"""

    return llm.invoke(prompt)