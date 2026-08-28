from pathlib import Path

from src.loaders.csv_loader import load_csv
from src.loaders.json_loader import load_json
from src.loaders.jsonl_loader import load_jsonl
from src.loaders.markdown_loader import load_markdown
from src.loaders.txt_loader import load_txt
from src.loaders.pdf_loader import load_pdf


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_all_documents(verbose=True):
    documents = []

    counts = {
        "csv": 0,
        "json": 0,
        "jsonl": 0,
        "md": 0,
        "txt": 0,
        "pdf": 0,
    }

    # CSV
    csv_files = [
        DATA / "structured" / "customers.csv",
        DATA / "structured" / "employees.csv",
        DATA / "structured" / "sales.csv",
        DATA / "semi_structured" / "system_logs.csv",
    ]

    for path in csv_files:
        docs = load_csv(path)

        documents.extend(docs)
        counts["csv"] += len(docs)

        if verbose:
            print(
                f"{path.name}: {len(docs)} chunks"
            )

    # JSON
    json_files = [
        DATA / "structured" / "products.json",
        DATA / "structured" / "stores.json",
    ]

    for path in json_files:
        docs = load_json(path)

        documents.extend(docs)
        counts["json"] += len(docs)

        if verbose:
            print(
                f"{path.name}: {len(docs)} chunks"
            )

    # JSONL
    path = (
        DATA
        / "semi_structured"
        / "tickets.jsonl"
    )

    docs = load_jsonl(path)

    documents.extend(docs)
    counts["jsonl"] += len(docs)

    if verbose:
        print(
            f"{path.name}: {len(docs)} chunks"
        )

    # Markdown
    for path in sorted(
        (DATA / "unstructured").rglob("*.md")
    ):
        docs = load_markdown(path)

        documents.extend(docs)
        counts["md"] += len(docs)

    if verbose:
        print(
            f"Markdown: {counts['md']} chunks"
        )

    # TXT
    for path in sorted(
        (DATA / "unstructured").rglob("*.txt")
    ):
        docs = load_txt(path)

        documents.extend(docs)
        counts["txt"] += len(docs)

    if verbose:
        print(
            f"TXT: {counts['txt']} chunks"
        )

    # PDF
    for path in sorted(
        (DATA / "unstructured").rglob("*.pdf")
    ):
        docs = load_pdf(path)

        documents.extend(docs)
        counts["pdf"] += len(docs)

    if verbose:
        print(
            f"PDF: {counts['pdf']} chunks"
        )

    return documents, counts