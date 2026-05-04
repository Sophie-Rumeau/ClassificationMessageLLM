import json
import re
from ollama import chat

ENTITY_KEYS = ["nom_animal", "espece", "numero_contrat"]
ESPECES_VALIDES = ["chien", "chat", "autre"]

SYSTEM_PROMPT = """
Tu es un extracteur d'entités pour des messages clients d'assurance animale.

Quand elles sont présentes, extrais exactement ces champs :
- nom_animal : le nom de l'animal mentionné
- espece : chien, chat, ou autre
- numero_contrat : le numéro de contrat si mentionné

Réponds uniquement en JSON valide avec exactement ces clés :
{
  "nom_animal": string ou null,
  "espece": "chien" | "chat" | "autre" | null,
  "numero_contrat": string ou null
}

Si une entité n'est pas présente, mets null.
"""


def _extraire_json(texte: str):
    match = re.search(r"\{.*\}", texte, flags=re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def _normaliser_espece(valeur):
    if valeur is None:
        return None

    texte = str(valeur).strip().lower()
    if texte in ESPECES_VALIDES:
        return texte

    if "chien" in texte:
        return "chien"
    if "chat" in texte:
        return "chat"
    return "autre"


def _normaliser_resultat(resultat):
    if not isinstance(resultat, dict):
        return {cle: None for cle in ENTITY_KEYS}

    return {
        "nom_animal": resultat.get("nom_animal") or None,
        "espece": _normaliser_espece(resultat.get("espece")),
        "numero_contrat": resultat.get("numero_contrat") or None,
    }


def extract_entities(content, model="ministral-3:3b-instruct-2512-q4_K_M"):
    response = chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
    )

    raw_response = response["message"]["content"].strip()
    parsed = _extraire_json(raw_response)

    if parsed is None:
        return {cle: None for cle in ENTITY_KEYS}

    return _normaliser_resultat(parsed)


def process_and_save(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for msg in data["messages"]:
        contenu = msg.get("contenu", "")
        entites = extract_entities(contenu)

        results.append(
            {
                "contenu": contenu,
                "nom_animal": entites["nom_animal"],
                "espece": entites["espece"],
                "numero_contrat": entites["numero_contrat"],
            }
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {"messages_entites": results},
            f,
            ensure_ascii=False,
            indent=2,
        )

    return results