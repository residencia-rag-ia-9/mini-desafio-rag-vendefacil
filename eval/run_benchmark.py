import json
from pathlib import Path

from src.generate import generate, search_engine
from src.retrieve import hybrid_search
from eval.judge_prompt import evaluate_answer


BENCHMARK = Path(
    "benchmark/questions_and_ground_truth.json"
)

RESULTS = Path("results.json")


def file_name(path):
    """Pega somente o nome do arquivo."""

    return Path(
        path.replace("\\", "/")
    ).name.lower()


def is_expected_refusal(question):
    """Verifica se o gabarito espera uma recusa."""

    metadata = question.get(
        "expected_metadata",
        {},
    )

    if metadata.get("sensitive"):
        return True

    if metadata.get("out_of_domain"):
        return True

    return False


def main():

    # Carrega o benchmark
    with open(
        BENCHMARK,
        encoding="utf-8",
    ) as file:
        benchmark = json.load(file)

    questions = benchmark["questions"]

    print(
        f"Perguntas encontradas: {len(questions)}"
    )

    # Carrega o mecanismo de busca uma vez
    db, documents, bm25, valid = search_engine()

    results = []

    for number, item in enumerate(
        questions,
        start=1,
    ):

        print("\n" + "=" * 60)
        print(
            f"{number}/{len(questions)} - {item['id']}"
        )
        print(item["question"])

        try:

            # Recupera os documentos
            filters, retrieved = hybrid_search(
                db,
                bm25,
                documents,
                valid,
                item["question"],
                use_filters=True,
            )

            # Gera a resposta
            response = generate(
                item["question"]
            )

            # -------------------------
            # Context Relevance
            # -------------------------

            expected_files = {
                file_name(source)
                for source
                in item["expected_sources"]
            }

            retrieved_files = {
                file_name(
                    doc.metadata.get(
                        "source_file",
                        "",
                    )
                )
                for doc in retrieved
            }

            if expected_files:

                context_relevance = (
                    len(
                        expected_files
                        & retrieved_files
                    )
                    / len(expected_files)
                )

            else:
                context_relevance = None

            # -------------------------
            # Citation Score
            # -------------------------

            if is_expected_refusal(item):

                citation_score = (
                    1.0
                    if response.is_refusal
                    else 0.0
                )

            else:

                used_files = {
                    file_name(source.filepath)
                    for source
                    in response.sources_used
                }

                citation_score = (
                    len(
                        expected_files
                        & used_files
                    )
                    / len(expected_files)
                    if expected_files
                    else 1.0
                )

            # -------------------------
            # Coerência da resposta
            # -------------------------

            should_refuse = (
                is_expected_refusal(item)
            )

            if should_refuse:

                coherence = (
                    1.0
                    if response.is_refusal
                    and response.confidence_level
                    == "recusado"
                    else 0.0
                )

            else:

                coherence = (
                    1.0
                    if not response.is_refusal
                    and response.sources_used
                    else 0.0
                )

            # -------------------------
            # LLM-as-judge
            # -------------------------

            evidences = [
                source.quotation
                for source
                in response.sources_used
            ]

            judge = evaluate_answer(
                item["question"],
                response.answer,
                item["ground_truth_answer"],
                evidences,
            )

            # Rubrica do professor:
            # 0.5 resposta
            # 0.3 citação
            # 0.2 coerência
            final_score = (
                0.5 * judge.correctness
                + 0.3 * citation_score
                + 0.2 * coherence
            )

            result = {
                "id": item["id"],
                "category": item["category"],
                "question": item["question"],
                "answer": response.answer,
                "filters": filters,
                "context_relevance":
                    context_relevance,
                "answer_relevance":
                    judge.answer_relevance,
                "groundedness":
                    judge.groundedness,
                "citation_score":
                    citation_score,
                "final_score":
                    final_score,
            }

            results.append(result)

            print(
                f"Nota: {final_score:.2f}"
            )

        except Exception as error:

            print("Erro:", error)

            results.append({
                "id": item["id"],
                "category": item["category"],
                "question": item["question"],
                "error": str(error),
            })

            # Se a API estiver sem saldo,
            # não adianta continuar chamando.
            if (
                "429" in str(error)
                or "insufficient_quota"
                in str(error)
            ):
                print(
                    "\nAPI sem cota. "
                    "Benchmark interrompido."
                )
                break

        # Salva a cada pergunta
        with open(
            RESULTS,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                results,
                file,
                ensure_ascii=False,
                indent=2,
            )

    # -------------------------
    # Resumo
    # -------------------------

    scores = [
        item["final_score"]
        for item in results
        if "final_score" in item
    ]

    print("\n" + "=" * 60)
    print("RESUMO")

    if scores:
        print(
            "Nota média:",
            round(
                sum(scores) / len(scores),
                2,
            ),
        )

    print(
        "Questões executadas:",
        len(results),
    )

    print(
        "Resultados salvos em results.json"
    )


if __name__ == "__main__":
    main()