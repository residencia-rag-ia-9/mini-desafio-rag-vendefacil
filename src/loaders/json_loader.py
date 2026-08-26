import json
from pathlib import Path

from langchain_core.documents import Document

from src.loaders.common import (
    clean,
    create_metadata,
    extract_filter_metadata,
    row_to_text,
)


JSON_CONFIG = {
    "products.json": {
        "doc_type": "product",
        "prefix": "Produto",
        "id_fields": [
            "product_id",
            "id",
            "sku",
        ],
    },

    "stores.json": {
        "doc_type": "store",
        "prefix": "Loja",
        "id_fields": [
            "store_id",
            "id",
        ],
    },
}


def get_records(data):

    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        for value in data.values():

            if isinstance(value, list):
                return value

        return [data]

    return []


def find_record_id(
    row: dict,
    fields: list,
    fallback: str,
):

    for field in fields:

        if row.get(field):
            return clean(row[field])

    return fallback


def load_json(path: Path) -> list[Document]:

    config = JSON_CONFIG.get(path.name)

    if config is None:
        raise ValueError(
            f"JSON não configurado: {path.name}"
        )

    with open(
        path,
        "r",
        encoding="utf-8-sig",
    ) as file:

        data = json.load(file)

    records = get_records(data)

    documents = []

    for index, row in enumerate(records, start=1):

        if not isinstance(row, dict):
            continue

        row = {
            key: clean(value)
            for key, value in row.items()
        }

        record_id = find_record_id(
            row,
            config["id_fields"],
            str(index),
        )

        prefix = (
            f"{config['prefix']} {record_id}"
        )

        text = row_to_text(
            row,
            prefix,
        )

        extra = extract_filter_metadata(row)

        metadata = create_metadata(
            path=path,
            doc_type=config["doc_type"],
            record_id=record_id,
            **extra,
        )

        documents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    return documents