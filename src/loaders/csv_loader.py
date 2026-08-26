import csv
from pathlib import Path

from langchain_core.documents import Document

from src.loaders.common import (
    clean,
    create_metadata,
    extract_filter_metadata,
    row_to_text,
)


CSV_CONFIG = {
    "customers.csv": {
        "doc_type": "customer",
        "id_field": "customer_id",
        "prefix": "Cliente",
    },

    "employees.csv": {
        "doc_type": "employee",
        "id_field": "id",
        "prefix": "Funcionário",
    },

    "sales.csv": {
        "doc_type": "sale",
        "id_field": None,
        "prefix": "Venda",
    },

    "system_logs.csv": {
        "doc_type": "log",
        "id_field": None,
        "prefix": "Log",
    },
}


def load_csv(path: Path) -> list[Document]:

    config = CSV_CONFIG.get(path.name)

    if config is None:
        raise ValueError(
            f"CSV não configurado: {path.name}"
        )

    documents = []

    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for index, row in enumerate(reader, start=1):

            row = {
                key: clean(value)
                for key, value in row.items()
            }

            id_field = config["id_field"]

            if id_field and row.get(id_field):
                record_id = row[id_field]
            else:
                record_id = str(index)

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