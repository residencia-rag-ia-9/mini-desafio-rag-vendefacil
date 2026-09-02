from src.generate import generate


def main():

    print("Assistente RAG - VendeFácil")

    while True:

        question = input(
            "\nPergunta ou 'sair': "
        )

        if question.lower() == "sair":
            break

        try:

            response = generate(question)

            print("\nResposta:")
            print(response.answer)

            print(
                "\nConfiança:",
                response.confidence_level,
            )

            if response.is_refusal:

                print(
                    "Motivo:",
                    response.refusal_reason,
                )

            else:

                print("\nFontes:")

                for source in (
                    response.sources_used
                ):

                    print(
                        source.filepath,
                        "-",
                        source.chunk_id,
                    )

        except Exception as error:

            print(
                "\nErro:",
                error,
            )


if __name__ == "__main__":
    main()