from collections import Counter

from langchain_community.vectorstores import FAISS

from src.ingest import INDEX_DIR, get_embeddings


QUESTIONS = [
    "Quais ações foram aprovadas sobre retenção de clientes?",
    "Qual foi a causa da queda do serviço de pagamento?",
    "Quais informações existem sobre segurança e LGPD?",
]


def load_index():
    """Carrega o FAISS já salvo."""
    return FAISS.load_local(
        str(INDEX_DIR),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def main():
    print("=" * 70)
    print("SANITY CHECK - ETAPA 1")
    print("=" * 70)

    print("\nCarregando índice salvo...")

    db = load_index()

    # Documentos já armazenados no FAISS
    documents = list(
        db.docstore._dict.values()
    )

    print(f"\nTotal de chunks: {len(documents)}")

    distribution = Counter(
        doc.metadata["doc_type"]
        for doc in documents
    )

    print("\nDistribuição por doc_type:")

    for doc_type, total in sorted(
        distribution.items()
    ):
        print(f"{doc_type}: {total}")

    # 3 perguntas, 5 resultados cada
    for question in QUESTIONS:

        print("\n" + "=" * 70)
        print(f"PERGUNTA: {question}")

        results = db.similarity_search(
            question,
            k=5,
        )

        for i, doc in enumerate(results, start=1):

            print(f"\n{i}. {doc.metadata['source_file']}")
            print(f"Chunk: {doc.metadata['chunk_id']}")
            print(doc.page_content[:250])


if __name__ == "__main__":
    main()