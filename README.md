# ClassificationMessageLLM

Projet de classification automatique de messages clients pour une assurance animale, avec extraction d'entités utiles dans les échanges.

Le projet s'appuie sur un modèle local via Ollama pour traiter les messages présents dans un fichier JSON, puis générer des sorties structurées au format JSON.

## Objectif

Pour chaque message client, le projet permet de :

1. attribuer une catégorie métier,
2. extraire les entités importantes présentes dans le texte,
3. produire un fichier JSON final exploitable.

### Catégories de classification

- `sinistre` : accident, maladie, hospitalisation, urgence vétérinaire
- `resiliation` : demande d'arrêt de contrat, décès de l'animal
- `question_contrat` : questions sur les garanties, formules, délais, couvertures
- `demande_remboursement` : envoi de facture, relance de remboursement
- `autre` : tout le reste, par exemple changement d'adresse ou réclamation technique

### Entités extraites

- `nom_animal` : nom de l'animal mentionné
- `espece` : `chien`, `chat` ou `autre`
- `numero_contrat` : numéro de contrat si présent dans le message

## Organisation du projet

### `src/`

Le dossier `src` contient les fichiers JSON liés aux données :

- `messages.json` : fichier original contenant les messages à traiter
- `messages_classes.json` : sortie de la classification seule
- `messages_entites.json` : sortie de l'extraction d'entités seule
- `resultats.json` : sortie finale combinant classification et entités

### `main/`

Le dossier `main` contient les fonctions Python et le point d'entrée du projet :

- `classifier.py` : classification d'un message dans une catégorie métier
- `extractIdentity.py` : extraction des entités du message
- `propre.py` : orchestration complète, combinant classification et extraction dans un seul JSON
- `main.py` : script principal pour lancer la génération des fichiers JSON

### `tests/`

Le dossier `tests` contient les scripts et notebooks de vérification :

- `testFonctionclassify_message.py` : test de la fonction de classification
- `readJson.ipynb` : exemples de lecture du JSON et d'accès aux messages
- `ollamaTest.ipynb` : test de connexion et d'appel au modèle via Ollama

## Flux de traitement

1. Lire `src/messages.json`.
2. Pour chaque message, appeler le classifieur.
3. Extraire les entités si elles sont présentes.
4. Regrouper les résultats dans une structure unique.
5. Écrire la sortie dans `src/resultats.json`.

Exemple de structure produite :

```json
{
	"resultats": [
		{
			"id": 1,
			"categorie": "sinistre",
			"entites": {
				"nom_animal": "Moustache",
				"espece": "chat",
				"numero_contrat": "SAV-2023-78542"
			}
		}
	]
}
```

## Prérequis

- Python 3.11 ou compatible avec l'environnement du projet
- Ollama installé et lancé localement
- Le modèle `ministral-3:3b-instruct-2512-q4_K_M` disponible dans Ollama

## Installation et lancement

Depuis le dossier `main`, exécuter le script principal :

```bash
python main.py
```

Le script génère le fichier final `src/resultats.json`.

## Exemples d'utilisation

### Classification seule

Dans `main/classifier.py`, la fonction principale est :

```python
classify_message(contenu)
```

Elle renvoie une catégorie comme `sinistre`, `resiliation`, `question_contrat`, `demande_remboursement` ou `autre`.

### Extraction d'entités seule

Dans `main/extractIdentity.py`, la fonction principale est :

```python
extract_entities(contenu)
```

Elle renvoie un dictionnaire avec `nom_animal`, `espece` et `numero_contrat`.

### Pipeline complet

Dans `main/propre.py`, la fonction :

```python
process_and_save(input_path, output_path)
```

combine les deux traitements et écrit un JSON complet au format attendu.

## Tests

- `tests/testFonctionclassify_message.py` permet de vérifier le retour de `classify_message` sur tous les messages du JSON.
- `tests/readJson.ipynb` montre comment lire le fichier JSON et accéder aux champs des messages.
- `tests/ollamaTest.ipynb` sert à tester l'appel au modèle Ollama.

## Remarque technique

Les imports dans le dossier `main` sont pensés pour être utilisés depuis ce dossier lors de l'exécution directe des scripts. C'est ce qui permet de lancer `python main.py` depuis `main/` sans modifier l'organisation du projet.