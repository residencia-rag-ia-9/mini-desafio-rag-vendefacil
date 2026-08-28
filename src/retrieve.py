import re
import unicodedata

from rank_bm25 import BM25Okapi
from langchain_community.vectorstores import FAISS

from src.ingest import INDEX_DIR, get_embeddings


# Nomes de estados usados nas perguntas
STATES = {
    "minas gerais": "MG",
    "sao paulo": "SP",
    "rio de janeiro": "RJ",
    "parana": "PR",
    "rio grande do sul": "RS",
    "santa catarina": "SC",
    "bahia": "BA",
    "pernambuco": "PE",
    "ceara": "CE",
    "goias": "GO",
    "espirito santo": "ES",
    "distrito federal": "DF",
}

MODULES = {
    "estoque": "estoque",
    "pdv": "pdv",
    "pay": "pay",
    "pagamento": "pay",
    "analytics": "analytics",
    "loja": "loja",
    "ecommerce": "loja",
    "e-commerce": "loja",
}


def normalize(text):
    """Minúsculo e sem acentos."""
    text = str(text).lower()

    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    ).strip()


def load_index():
    """Carrega o FAISS já criado."""
    return FAISS.load_local(
        str(INDEX_DIR),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def valid_values(documents):
    """Valores que realmente existem nos metadados."""
    values = {
        "state": set(),
        "module": set(),
        "doc_type": set(),
    }

    for doc in documents:
        meta = doc.metadata

        for field in values:
            value = meta.get(field)

            if isinstance(value, list):
                values[field].update(
                    normalize(v) for v in value
                )

            elif value:
                values[field].add(
                    normalize(value)
                )

    return values


def analyze_query(query, valid):
    """Extrai filtros simples da pergunta."""
    text = normalize(query)
    filters = {}

    # Estado por nome
    for name, state in STATES.items():
        if name in text:
            filters["state"] = state
            break

    # Estado pela sigla
    if "state" not in filters:
        match = re.search(
            r"\b(MG|SP|RJ|PR|RS|SC|BA|PE|CE|GO|ES|DF)\b",
            query.upper(),
        )

        if match:
            filters["state"] = match.group(1)

    # Módulo
    for word, module in MODULES.items():
        if word in text:
            filters["module"] = module
            break

    # Tipo de documento
    if "ticket" in text or "chamado" in text:
        filters["doc_type"] = "ticket"

    # Valida contra os valores do índice
    return {
        field: value
        for field, value in filters.items()
        if normalize(value) in valid[field]
    }


def match_metadata(metadata, filters):
    """Verifica se o chunk passa nos filtros."""
    for field, expected in filters.items():

        value = metadata.get(field)

        if isinstance(value, list):

            if normalize(expected) not in {
                normalize(v) for v in value
            }:
                return False

        elif normalize(value) != normalize(expected):
            return False

    return True


def dense_search(db, query, filters, total, k=10):
    """Busca vetorial no FAISS."""
    if not filters:
        return db.similarity_search(query, k=k)

    return db.similarity_search(
        query,
        k=k,
        fetch_k=total,
        filter=lambda meta: match_metadata(
            meta,
            filters,
        ),
    )


def bm25_search(bm25, documents, query, filters, k=10):
    """Busca por palavras usando BM25."""
    scores = bm25.get_scores(
        normalize(query).split()
    )

    order = sorted(
        range(len(documents)),
        key=lambda i: scores[i],
        reverse=True,
    )

    results = []

    for i in order:
        doc = documents[i]

        if filters and not match_metadata(
            doc.metadata,
            filters,
        ):
            continue

        results.append(doc)

        if len(results) == k:
            break

    return results


def rrf(dense, sparse, k=60, top_k=5):
    """Junta os rankings Dense e BM25."""
    scores = {}
    documents = {}

    for ranking in (dense, sparse):

        for position, doc in enumerate(
            ranking,
            start=1,
        ):
            chunk_id = doc.metadata["chunk_id"]

            scores[chunk_id] = (
                scores.get(chunk_id, 0)
                + 1 / (k + position)
            )

            documents[chunk_id] = doc

    ranking = sorted(
        scores,
        key=scores.get,
        reverse=True,
    )

    return [
        documents[chunk_id]
        for chunk_id in ranking[:top_k]
    ]


def hybrid_search(
    db,
    bm25,
    documents,
    valid,
    query,
    use_filters=True,
):
    """Busca final: Dense + BM25 + RRF."""
    filters = (
        analyze_query(query, valid)
        if use_filters
        else {}
    )

    dense = dense_search(
        db,
        query,
        filters,
        len(documents),
    )

    sparse = bm25_search(
        bm25,
        documents,
        query,
        filters,
    )

    return filters, rrf(
        dense,
        sparse,
    )


def main():
    print("=" * 70)
    print("ETAPA 2 - BUSCA HÍBRIDA")
    print("=" * 70)

    db = load_index()

    documents = list(
        db.docstore._dict.values()
    )

    # Índice BM25
    bm25 = BM25Okapi([
        normalize(doc.page_content).split()
        for doc in documents
    ])

    valid = valid_values(documents)

    questions = [
        "Quais tickets de Minas Gerais estão relacionados ao módulo de estoque?",
        "Quais tickets de São Paulo estão relacionados ao módulo Pay?",
        "Quais tickets do Rio de Janeiro estão relacionados ao módulo PDV?",
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print(f"PERGUNTA: {question}")

        # Sem filtro
        _, results = hybrid_search(
            db,
            bm25,
            documents,
            valid,
            question,
            use_filters=False,
        )

        print("\nSEM FILTRO:")

        for doc in results:
            print(
                "-",
                doc.metadata["source_file"],
                doc.metadata["chunk_id"],
            )

        # Com filtro
        filters, results = hybrid_search(
            db,
            bm25,
            documents,
            valid,
            question,
            use_filters=True,
        )

        print(f"\nFILTROS: {filters}")
        print("COM FILTRO:")

        for doc in results:
            print(
                "-",
                doc.metadata["source_file"],
                doc.metadata["chunk_id"],
            )


if __name__ == "__main__":
    main()