import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.loaders.common import create_metadata


TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
)

MESSAGE_PATTERN = re.compile(
    r"(?=^(?:De|From|Remetente):)",
    flags=re.IGNORECASE | re.MULTILINE,
)


SENSITIVE_TERMS = [
    "senha",
    "password",
    "token",
    "credencial",
    "chave api",
    "chave de api",
    "postgres",
    "root",
    "cpf",
    "cvv",
]


def get_customer_id(path: Path):
    match = re.match(
        r"customer_(\d+)_",
        path.name,
        re.IGNORECASE,
    )

    if not match:
        return None

    return f"CUST{int(match.group(1)):03d}"


def get_module(path: Path):
    name = path.name.lower()

    if "estoque" in name:
        return "estoque"

    if "ecommerce" in name:
        return "ecommerce"

    if "analytics" in name:
        return "analytics"

    if "pdv" in name:
        return "pdv"

    if "tef" in name or "pix" in name:
        return "pay"

    return None


def sensitivity(text: str):
    normalized = text.lower()

    for term in SENSITIVE_TERMS:
        if term in normalized:
            return "restrito"

    return "interno"


def load_txt(path: Path):
    text = path.read_text(
        encoding="utf-8-sig",
        errors="replace",
    ).strip()

    if not text:
        return []

    messages = [
        item.strip()
        for item in MESSAGE_PATTERN.split(text)
        if item.strip()
    ]

    if not messages:
        messages = [text]

    customer_id = get_customer_id(path)
    module = get_module(path)

    documents = []

    for message_number, message in enumerate(
        messages,
        start=1,
    ):
        if len(message) > 1800:
            chunks = TEXT_SPLITTER.split_text(message)
        else:
            chunks = [message]

        for chunk_number, chunk in enumerate(
            chunks,
            start=1,
        ):
            extra = {
                "sensitivity": sensitivity(chunk),
            }

            if customer_id:
                extra["customer_id"] = customer_id

            if module:
                extra["module"] = module

            metadata = create_metadata(
                path,
                "email",
                f"{message_number}_{chunk_number}",
                **extra,
            )

            documents.append(
                Document(
                    page_content=chunk,
                    metadata=metadata,
                )
            )

    return documents