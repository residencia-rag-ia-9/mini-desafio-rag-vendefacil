from typing import Literal

from pydantic import BaseModel, Field, model_validator


class SourceEvidence(BaseModel):
    """Fonte usada na resposta."""

    filepath: str
    chunk_id: str
    quotation: str = Field(max_length=500)


class RAGResponse(BaseModel):
    """Formato obrigatório da resposta."""

    answer: str

    confidence_level: Literal[
        "alta",
        "media",
        "baixa",
        "recusado",
    ]

    sources_used: list[SourceEvidence]

    reasoning: str

    is_refusal: bool

    refusal_reason: Literal[
        "lgpd",
        "fora_de_escopo",
        "sem_evidencia",
    ] | None = None

    @model_validator(mode="after")
    def validate_response(self):
        """Garante consistência da resposta."""

        if self.is_refusal:

            if self.sources_used:
                raise ValueError(
                    "Recusa não pode ter fontes."
                )

            if self.confidence_level != "recusado":
                raise ValueError(
                    "Recusa deve ter confiança 'recusado'."
                )

            if self.refusal_reason is None:
                raise ValueError(
                    "Recusa precisa de motivo."
                )

        else:

            if not self.sources_used:
                raise ValueError(
                    "Resposta precisa de evidência."
                )

            if self.confidence_level == "recusado":
                raise ValueError(
                    "Resposta válida não pode ser recusada."
                )

        return self