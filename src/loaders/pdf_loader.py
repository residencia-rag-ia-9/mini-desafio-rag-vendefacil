from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.loaders.common import create_metadata


PDF_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
)


def load_pdf(path: Path):
    reader = PdfReader(str(path))

    documents = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        text = (
            page.extract_text()
            or ""
        ).strip()

        if not text:
            continue

        chunks = PDF_SPLITTER.split_text(text)

        for chunk_number, chunk in enumerate(
            chunks,
            start=1,
        ):
            metadata = create_metadata(
                path,
                "policy",
                f"page_{page_number}_{chunk_number}",
                page=page_number,
            )

            documents.append(
                Document(
                    page_content=chunk,
                    metadata=metadata,
                )
            )

    return documents