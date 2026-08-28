import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.loaders.common import (
    clean,
    create_metadata,
    extract_filter_metadata,
)


BODY_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def load_jsonl(path: Path) -> list[Document]:
    documents = []

    with open(path, "r", encoding="utf-8-sig") as file:

        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            row = json.loads(line)

            ticket_id = clean(row.get("ticket_id"))

            if not ticket_id:
                ticket_id = str(line_number)

            header = (
                f"Ticket {ticket_id}. "
                f"Cliente: {clean(row.get('customer_name'))}. "
                f"Customer ID: {clean(row.get('customer_id'))}. "
                f"Estado: {clean(row.get('state'))}. "
                f"Módulo: {clean(row.get('module'))}. "
                f"Título: {clean(row.get('title'))}. "
                f"Prioridade: {clean(row.get('priority'))}. "
                f"Status: {clean(row.get('status'))}. "
                f"Categoria: {clean(row.get('category'))}. "
                f"Data: {clean(row.get('created_at'))}. "
            )

            body = (
                f"Descrição: {clean(row.get('description'))}. "
                f"Resolução: {clean(row.get('resolution'))}. "
                f"Sentimento: {clean(row.get('sentiment'))}."
            )

            if len(body) > 1800:
                parts = BODY_SPLITTER.split_text(body)
            else:
                parts = [body]

            extra = extract_filter_metadata(row)

            for part_number, part in enumerate(parts, start=1):

                text = header + part

                metadata = create_metadata(
                    path=path,
                    doc_type="ticket",
                    record_id=f"{ticket_id}_{part_number}",
                    **extra,
                )

                documents.append(
                    Document(
                        page_content=text,
                        metadata=metadata,
                    )
                )

    return documents