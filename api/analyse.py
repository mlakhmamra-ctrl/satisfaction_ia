import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

def analyser_commentaire(texte: str) -> dict:
    prompt = f"""
Tu es un expert en analyse de satisfaction client.
Analyse ce texte et réponds UNIQUEMENT en JSON valide.

TEXTE: {texte}

JSON:
{{
    "sentiment": {{"emotion": "joie ou colere ou tristesse ou neutre", "score": 0.95}},
    "ces": {{"score": 5.0, "niveau": "facile ou moyen ou difficile"}},
    "rca": {{"cause": "cause principale", "categorie": "reseau ou materiel ou logiciel ou humain"}},
    "escalade": {{"necessaire": false, "niveau": "faible ou moyen ou critique"}},
    "sla": {{"respecte": true}},
    "resume": "resume court"
}}
"""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=120
    )

    if response.status_code == 200:
        result = response.json()
        return json.loads(result['response'])
    else:
        raise Exception(f"Erreur: {response.status_code}")


# TEST DIRECT
if __name__ == "__main__":
    
    # Test 1 — Client satisfait
    print("=== TEST 1 — Client satisfait ===")
    resultat = analyser_commentaire("Excellent service, technicien très compétent !")
    print(json.dumps(resultat, ensure_ascii=False, indent=2))

    # Test 2 — Client insatisfait
    print("\n=== TEST 2 — Client insatisfait ===")
    resultat = analyser_commentaire("Très mauvais service, problème non résolu !")
    print(json.dumps(resultat, ensure_ascii=False, indent=2))

    # Test 3 — Conversation ticket sans réponse client
    print("\n=== TEST 3 — Conversation ticket ===")
    conversation = """
    Client: Internet ne fonctionne pas depuis ce matin
    Tech: Je regarde le problème
    Client: Toujours pas résolu après 3 heures !
    Tech: Problème DNS corrigé
    Solution: Configuration DNS mise à jour
    """
    resultat = analyser_commentaire(conversation)
    print(json.dumps(resultat, ensure_ascii=False, indent=2))