from classifier import process_and_save
from extractIdentity import process_and_save as process_and_save_identity


def main():
    input_path = "../src/messages.json"
    output_path = "../src/messages_classes.json"

    results = process_and_save(input_path, output_path)

    print("Classification terminée.")
    print(f"{len(results)} messages traités.")
    print(f"Résultat écrit dans : {output_path}")

    results_identity = process_and_save_identity(input_path, "../src/messages_entites.json")
    print("Extraction d'identité terminée.")
    print(f"{len(results_identity)} messages traités.")
    print(f"Résultat écrit dans : ../src/messages_entites.json")


if __name__ == "__main__":
    main()