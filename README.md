\# Satisfaction Client IA — GLPI



\## Description

Analyse automatique de la satisfaction client GLPI via Ollama + Qwen2.5.

Pas de serveur web — exécution directe en Python.



\## Ce que ça fait

\- Détecte le sentiment (joie, colère, tristesse, neutre)

\- Calcule le score CES (Customer Effort Score)

\- Identifie la cause racine (RCA)

\- Détecte si une escalade est nécessaire

\- Vérifie le respect du SLA

\- Génère un résumé automatique



\## Prérequis

\- Python 3.10+

\- Ollama installé

\- Modèle Qwen2.5:3b téléchargé



\## Installation



\### 1. Installer Ollama

https://ollama.com/download



\### 2. Télécharger le modèle

ollama pull qwen2.5:3b



\### 3. Installer les dépendances

pip install -r api/requirements.txt



\## Utilisation



\### Lancer l'analyse

cd api

python app.py



\### Exemple de résultat

```json

{

&#x20; "sentiment": { "emotion": "joie", "score": 0.95 },

&#x20; "ces": { "score": 5.0, "niveau": "facile" },

&#x20; "rca": { "cause": "technicien compétent", "categorie": "humain" },

&#x20; "escalade": { "necessaire": false, "niveau": "faible" },

&#x20; "sla": { "respecte": true },

&#x20; "resume": "Excellent service, satisfaction élevée."

}

```



\## Structure du projet

```

satisfaction\_ia/

├── api/

│   ├── app.py            # Moteur d'analyse Ollama + Qwen2.5

│   ├── analyse.py        # Scripts de test

│   └── requirements.txt

└── README.md

```





