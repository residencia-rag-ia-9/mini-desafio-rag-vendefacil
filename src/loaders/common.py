import hashlib
import json
import unicodedata
from pathlib import Path


REQUIRED_METADATA = {
    "source_file",
    "doc_type",
    "chunk_id",
    "sensitivity",
}


def clean(value) -> str:
    if value is None:
        return ""

    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)

    return str(value).strip()


def remove_accents(text: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(char)
    )


def normalize_module(value: str) -> str:
    text = remove_accents(clean(value)).lower()

    text = text.replace("vendefacil", "").strip()

    aliases = {
        "loja": "ecommerce",
        "e-commerce": "ecommerce",
        "e commerce": "ecommerce",
        "pagamento": "pay",
        "pagamentos": "pay",
    }

    return aliases.get(text, text)


def stable_id(*values) -> str:
    raw = "|".join(clean(value) for value in values)

    return hashlib.sha1(
        raw.encode("utf-8")
    ).hexdigest()[:12]


def get_sensitivity(doc_type: str) -> str:
    levels = {
        "customer": "interno",
        "employee": "restrito",
        "sale": "interno",
        "log": "restrito",
        "product": "publico",
        "store": "publico",
    }

    return levels.get(doc_type, "interno")


def extract_filter_metadata(row: dict) -> dict:
    metadata = {}

    if row.get("customer_id"):
        metadata["customer_id"] = clean(row["customer_id"])

    if row.get("state"):
        metadata["state"] = clean(row["state"]).upper()

    if row.get("priority"):
        metadata["priority"] = clean(row["priority"]).lower()

    if row.get("status"):
        metadata["status"] = clean(row["status"]).lower()

    module = row.get("module") or row.get("main_product")

    if module:
        metadata["module"] = normalize_module(module)

    date = (
        row.get("date")
        or row.get("created_at")
        or row.get("timestamp")
        or row.get("hire_date")
    )

    if date:
        metadata["date"] = clean(date)

    return metadata


def create_metadata(
    path: Path,
    doc_type: str,
    record_id: str,
    **extra,
) -> dict:

    metadata = {
        "source_file": path.name,
        "doc_type": doc_type,
        "chunk_id": f"{doc_type}_{stable_id(path.name, record_id)}",
        "sensitivity": get_sensitivity(doc_type),
    }

    for key, value in extra.items():
        value = clean(value)

        if value:
            metadata[key] = value

    return metadata


def row_to_text(row: dict, prefix: str) -> str:
    fields = []

    for key, value in row.items():
        value = clean(value)

        if not value:
            continue

        readable_key = key.replace("_", " ")

        fields.append(
            f"{readable_key}: {value}"
        )

    return f"{prefix}. " + ". ".join(fields) + "."


def validate_documents(documents):
    errors = []

    for index, document in enumerate(documents, start=1):

        missing = REQUIRED_METADATA - set(
            document.metadata.keys()
        )

        if missing:
            errors.append(
                f"Documento {index}: faltando {missing}"
            )

        if not document.page_content.strip():
            errors.append(
                f"Documento {index}: conteúdo vazio"
            )

    if errors:
        for error in errors:
            print(error)

        raise RuntimeError(
            "Existem chunks inválidos."
        )

    print(
        f"Validação OK: {len(documents)} chunks válidos."
    )