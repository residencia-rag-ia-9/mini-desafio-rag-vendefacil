from collections import Counter
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from src.load_all import load_all_documents
from src.loaders.common import validate_documents


ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "index"

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )


def main():
    print("=" * 70)
    print("ETAPA 1 - INDEXAÇÃO VETORIAL")
    print("=" * 70)

    print("\n1. Carregando documentos...")

    documents, counts = load_all_documents()

    print("\n2. Validando documentos...")

    validate_documents(documents)

    print(
        f"\nTotal: {len(documents)} chunks"
    )

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

    print("\n3. Carregando modelo de embeddings...")

    embeddings = get_embeddings()

    print(
        "\n4. Criando índice FAISS..."
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )

    INDEX_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "\n5. Salvando índice..."
    )

    vector_store.save_local(
        str(INDEX_DIR)
    )

    print(
        f"\nÍndice salvo em: {INDEX_DIR}"
    )

    print("\nETAPA DE INGESTÃO CONCLUÍDA.")


if __name__ == "__main__":
    main()