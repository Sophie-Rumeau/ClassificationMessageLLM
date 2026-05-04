import json
from classifier import classify_message
from extractIdentity import extract_entities


def construire_resultats(messages):
	resultats = []

	for message in messages:
		contenu = message.get("contenu", "")

		resultats.append(
			{
				"id": message.get("id"),
				"categorie": classify_message(contenu),
				"entites": extract_entities(contenu),
			}
		)

	return resultats


def process_and_save(input_path, output_path):
	with open(input_path, "r", encoding="utf-8") as fichier:
		data = json.load(fichier)

	resultats = construire_resultats(data.get("messages", []))

	output_data = {"resultats": resultats}

	with open(output_path, "w", encoding="utf-8") as fichier:
		json.dump(output_data, fichier, ensure_ascii=False, indent=2)

	return output_data


def main():
	input_path = "../src/messages.json"
	output_path = "../src/resultats.json"
	process_and_save(input_path, output_path)


if __name__ == "__main__":
	main()
