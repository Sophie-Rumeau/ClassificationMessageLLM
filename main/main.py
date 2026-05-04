from classifier import process_and_save


def main():
    input_path = "../src/messages.json"
    output_path = "../src/messages_classes.json"

    results = process_and_save(input_path, output_path)

    print("Classification terminée.")
    print(f"{len(results)} messages traités.")
    print(f"Résultat écrit dans : {output_path}")


if __name__ == "__main__":
    main()