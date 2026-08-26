from collections import Counter

from src.load_all import load_all_documents
from src.loaders.common import validate_documents


def main():
    print("=" * 70)
    print("TESTE COMPLETO DOS LOADERS")
    print("=" * 70)

    documents, counts = load_all_documents()

    print("\nVALIDANDO METADADOS...")

    validate_documents(documents)

    print("\nCHUNKS POR FORMATO:")

    for format_name, total in counts.items():
        print(f"{format_name}: {total}")

        if total == 0:
            raise RuntimeError(
                f"Nenhum documento do formato {format_name}"
            )

    distribution = Counter(
        doc.metadata["doc_type"]
        for doc in documents
    )

    print("\nDISTRIBUIÇÃO POR DOC_TYPE:")

    for doc_type, total in sorted(
        distribution.items()
    ):
        print(
            f"{doc_type}: {total}"
        )

    print("\n" + "=" * 70)

    print(
        f"TOTAL GERAL: {len(documents)} chunks"
    )

    print(
        "TODOS OS 6 FORMATOS FORAM TESTADOS."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()