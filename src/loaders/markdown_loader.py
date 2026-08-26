from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from src.loaders.common import create_metadata


HEADER_SPLITTER = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
    ],
    strip_headers=False,
)

LONG_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
)

MODULES = {
    "pdv",
    "pay",
    "analytics",
    "estoque",
    "ecommerce",
}


def classify_document(path: Path):
    parts = [part.lower() for part in path.parts]

    if "meetings" in parts:
        return "ata", None

    if "policies" in parts:
        return "policy", None

    if "documentation" in parts:
        for module in MODULES:
            if module in parts:
                return "manual", module

        return "manual", None

    return "manual", None


def load_markdown(path: Path):
    text = path.read_text(
        encoding="utf-8-sig",
        errors="replace",
    )

    doc_type, module = classify_document(path)

    sections = HEADER_SPLITTER.split_text(text)

    documents = []

    for section_number, section in enumerate(
        sections,
        start=1,
    ):
        content = section.page_content.strip()

        if not content:
            continue

        section_name = (
            section.metadata.get("h3")
            or section.metadata.get("h2")
            or section.metadata.get("h1")
            or f"secao_{section_number}"
        )

        if len(content) > 1500:
            chunks = LONG_SPLITTER.split_text(content)
        else:
            chunks = [content]

        for chunk_number, chunk in enumerate(
            chunks,
            start=1,
        ):
            extra = {
                "section": section_name,
            }

            if module:
                extra["module"] = module

            if doc_type == "ata":
                possible_date = path.stem[:7]

                if (
                    len(possible_date) == 7
                    and possible_date[4] == "-"
                ):
                    extra["date"] = possible_date

            metadata = create_metadata(
                path,
                doc_type,
                f"{section_number}_{chunk_number}",
                **extra,
            )

            documents.append(
                Document(
                    page_content=chunk,
                    metadata=metadata,
                )
            )

    return documents