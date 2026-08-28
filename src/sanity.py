from collections import Counter
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "index"

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def main():
    print("=" * 70)
    print("SANITY CHECK - ETAPA 1")
    print("=" * 70)

    if not INDEX_DIR.exists():
        raise RuntimeError(
            "Índice não encontrado. Execute primeiro: python -m src.ingest"
        )

    print("\nRecarregando FAISS SEM reindexar...")

    embeddings = get_embeddings()

    db = FAISS.load_local(
        str(INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    documents = list(
        db.docstore._dict.values()
    )

    print(
        f"\nTOTAL DE CHUNKS: {len(documents)}"
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

    questions = [
        "Como funciona o reembolso de despesas?",
        "Quais problemas de estoque aparecem nos tickets?",
        "Quais erros relacionados ao PDV aparecem nos logs?",
    ]

    for question in questions:
        print("\n" + "=" * 70)
        print(f"PERGUNTA: {question}")
        print("=" * 70)

        results = db.similarity_search(
            question,
            k=5,
        )

        for position, doc in enumerate(
            results,
            start=1,
        ):
            print(
                f"\nRESULTADO {position}"
            )

            print(
                "Arquivo:",
                doc.metadata.get("source_file"),
            )

            print(
                "Tipo:",
                doc.metadata.get("doc_type"),
            )

            print(
                "Sensibilidade:",
                doc.metadata.get("sensitivity"),
            )

            print(
                "Chunk:",
                doc.metadata.get("chunk_id"),
            )

            print(
                "\nTexto:"
            )

            print(
                doc.page_content[:500]
            )


if __name__ == "__main__":
    main()