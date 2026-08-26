from pathlib import Path
from collections import Counter

from src.loaders.csv_loader import load_csv
from src.loaders.json_loader import load_json
from src.loaders.common import validate_documents


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main():

    documents = []

    csv_files = [
        DATA / "structured" / "customers.csv",
        DATA / "structured" / "employees.csv",
        DATA / "structured" / "sales.csv",
        DATA / "semi_structured" / "system_logs.csv",
    ]

    json_files = [
        DATA / "structured" / "products.json",
        DATA / "structured" / "stores.json",
    ]

    print("=" * 60)
    print("TESTE DA PARTE DO LUIZ")
    print("=" * 60)

    for path in csv_files:

        docs = load_csv(path)

        documents.extend(docs)

        print(
            f"{path.name}: {len(docs)} chunks"
        )

    for path in json_files:

        docs = load_json(path)

        documents.extend(docs)

        print(
            f"{path.name}: {len(docs)} chunks"
        )

    print()

    validate_documents(documents)

    distribution = Counter(
        doc.metadata["doc_type"]
        for doc in documents
    )

    print("\nDistribuição:")

    for doc_type, total in sorted(
        distribution.items()
    ):
        print(
            f"{doc_type}: {total}"
        )

    print("\n" + "=" * 60)
    print("EXEMPLO DE CHUNK")
    print("=" * 60)

    print(
        documents[0].page_content
    )

    print("\nMetadados:")

    print(
        documents[0].metadata
    )


if __name__ == "__main__":
    main()