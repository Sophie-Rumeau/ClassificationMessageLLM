import json
from ollama import chat

CATEGORIES = [
    "sinistre",
    "resiliation",
    "question_contrat",
    "demande_remboursement",
    "autre"
]

SYSTEM_PROMPT = """
Tu es un classificateur de messages client pour une assurance animale.

Attribuer une catégorie parmi :
• sinistre : accident, maladie, hospitalisation, urgence vétérinaire
• resiliation : demande d'arrêt de contrat, décès de l'animal
• question_contrat : questions sur les garanties, formules, délais, couvertures
• demande_remboursement : envoi de facture, relance de remboursement
• autre : tout le reste (changement d'adresse, réclamation technique, etc.)

Si le message est ambigu, réponds uniquement : besoin_precision
"""

def classify_message(content, model="ministral-3:3b-instruct-2512-q4_K_M"):
    response = chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
        ],
    )
    return response["message"]["content"].strip().lower()


def ask_clarification(content, model="ministral-3:3b-instruct-2512-q4_K_M"):
    prompt = f"""
Le message suivant est ambigu :
"{content}"

Pose UNE question courte pour clarifier.
"""
    response = chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"].strip()


def process_and_save(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for msg in data["messages"]:
        contenu = msg.get("contenu", "")

        category = classify_message(contenu)

        entry = {
            "contenu": contenu,
            "categorie": None,
            "clarification": None
        }

        if category == "besoin_precision":
            entry["clarification"] = ask_clarification(contenu)
        else:
            if category not in CATEGORIES:
                category = "autre"
            entry["categorie"] = category

        results.append(entry)

    # écriture dans un fichier JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {"messages_classes": results},
            f,
            ensure_ascii=False,
            indent=2
        )

    return results