\# Satisfaction Client IA — GLPI Plugin



\## Description

API Flask + Qwen2.5 pour analyser la satisfaction client GLPI.



\## Prérequis

\- Python 3.10+

\- Ollama installé

\- Qwen2.5:3b téléchargé



\## Installation



\### 1. Installer Ollama

https://ollama.com/download



\### 2. Télécharger Qwen

ollama pull qwen2.5:3b



\### 3. Installer les dépendances

pip install -r requirements.txt



\### 4. Lancer l'API

cd api

python app.py



\## Utilisation



\### Test santé

GET http://localhost:5000/health



\### Analyser un commentaire

POST http://localhost:5000/analyse

{

&#x20;   "commentaire": "Excellent service !"

}



\### Analyser un ticket GLPI

GET http://localhost:5000/analyse/ticket/1

