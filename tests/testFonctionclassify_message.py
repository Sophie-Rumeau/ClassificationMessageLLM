import json

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main.classifier import classify_message

def main():
    input_path = "../src/messages.json"
    with open(input_path, 'r') as f:
        messagesFile = json.load(f)
    
    results = []
    for msg in messagesFile["messages"]:
        results.append(classify_message(msg["contenu"]))

    print(results)


if __name__ == "__main__":
    main()


# (VenvSanteVet_py311) yukiyamato@MacBook-Pro-de-Yuki tests % python testFonctionclassify_message.py
# ['**sinistre**', '**sinistre**', '**question_contrat**', '**demande_remboursement**', '**autre**', '**sinistre**', '**sinistre**', '**question_contrat**', '**demande_remboursement**', '**sinistre**', '**sinistre**', '**resiliation**', '**question_contrat**', '**demande_remboursement**', '**sinistre**', '**question_contrat**', '**remboursement**', '**question_contrat**', '**demande_remboursement**', '**sinistre**', '**demande_remboursement**', "**sinistre** *(décès de l'animal, mais lié à une demande de clôture de contrat)*", '**sinistre**', '**besoin_precision**', '**sinistre**']
# (VenvSanteVet_py311) yukiyamato@MacBook-Pro-de-Yuki tests % 