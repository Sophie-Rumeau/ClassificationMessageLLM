from classifier import process_and_save
from extractIdentity import process_and_save as process_and_save_identity
from propre import process_and_save as process_and_save_propre


def main():
    input_path = "../src/messages.json"
    output_path = "../src/messages_classes.json"

    # results = process_and_save(input_path, output_path)

    # print("Classification terminée.")
    # print(f"{len(results)} messages traités.")
    # print(f"Résultat écrit dans : {output_path}")

    # results_identity = process_and_save_identity(input_path, "../src/messages_entites.json")
    # print("Extraction d'identité terminée.")
    # print(f"{len(results_identity)} messages traités.")
    # print(f"Résultat écrit dans : ../src/messages_entites.json")
    
    results_propre = process_and_save_propre(input_path, "../src/resultats.json")
    print("Classification et extraction d'identité terminées.")
    print(f"{len(results_propre['resultats'])} messages traités.")
    print(f"Résultat écrit dans : ../src/resultats.json")


if __name__ == "__main__":
    main()