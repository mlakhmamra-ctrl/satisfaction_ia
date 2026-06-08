from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

def analyser_avec_qwen(texte: str) -> dict:
    prompt = f"""
Tu es un expert en analyse de satisfaction client pour un service informatique.
Analyse ce texte et réponds UNIQUEMENT en JSON valide.

TEXTE A ANALYSER:
{texte}

Réponds avec ce JSON exact:
{{
    "sentiment": {{
        "emotion": "joie ou colere ou tristesse ou peur ou neutre",
        "score": 0.95,
        "explication": "explication courte"
    }},
    "ces": {{
        "score": 5.0,
        "niveau": "facile ou moyen ou difficile",
        "explication": "explication courte"
    }},
    "rca": {{
        "cause": "cause principale",
        "categorie": "reseau ou materiel ou logiciel ou humain ou autre",
        "recurrent": false
    }},
    "escalade": {{
        "necessaire": false,
        "niveau": "faible ou moyen ou critique",
        "raison": "raison courte"
    }},
    "sla": {{
        "respecte": true,
        "commentaire": "commentaire court"
    }},
    "resume": "resume global court"
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
        raise Exception(f"Erreur Ollama: {response.status_code}")


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model": MODEL})


@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Données manquantes"}), 400

    # Construire le texte à analyser
    texte = ""
    
    if data.get('commentaire'):
        texte += f"Commentaire client: {data['commentaire']}\n"
    
    if data.get('conversation'):
        texte += f"Conversation:\n{data['conversation']}\n"
    
    if data.get('solution'):
        texte += f"Solution apportée: {data['solution']}\n"

    if not texte:
        return jsonify({"error": "Aucun texte à analyser"}), 400

    try:
        resultat = analyser_avec_qwen(texte)
        resultat['source'] = 'commentaire' if data.get('commentaire') else 'conversation'
        resultat['client_responded'] = 1 if data.get('commentaire') else 0
        return jsonify(resultat)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/analyse/ticket/<int:ticket_id>', methods=['GET'])
def analyse_ticket(ticket_id):
    """Analyse automatique d'un ticket sans réponse client"""
    import pymysql
    
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='glpi',
            charset='utf8mb4'
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Lire le ticket
        cursor.execute("""
            SELECT t.name, t.content, t.priority, t.date_creation
            FROM glpi_tickets t
            WHERE t.id = %s
        """, (ticket_id,))
        ticket = cursor.fetchone()

        if not ticket:
            return jsonify({"error": "Ticket introuvable"}), 404

        # Lire les suivis (conversation)
        cursor.execute("""
            SELECT f.content, u.name as auteur, f.date
            FROM glpi_itilfollowups f
            LEFT JOIN glpi_users u ON f.users_id = u.id
            WHERE f.items_id = %s AND f.itemtype = 'Ticket'
            ORDER BY f.date ASC
        """, (ticket_id,))
        suivis = cursor.fetchall()

        # Lire la solution
        cursor.execute("""
            SELECT content FROM glpi_itilsolutions
            WHERE items_id = %s AND itemtype = 'Ticket'
            ORDER BY id DESC LIMIT 1
        """, (ticket_id,))
        solution = cursor.fetchone()

        conn.close()

        # Construire la conversation
        conversation = f"Titre: {ticket['name']}\n"
        conversation += f"Description: {ticket['content']}\n\n"
        
        if suivis:
            conversation += "=== MESSAGES ===\n"
            for suivi in suivis:
                conversation += f"[{suivi['date']}] {suivi['auteur']}: {suivi['content']}\n"

        if solution:
            conversation += f"\n=== SOLUTION ===\n{solution['content']}"

        # Analyser avec Qwen
        resultat = analyser_avec_qwen(conversation)
        resultat['source'] = 'conversation'
        resultat['client_responded'] = 0
        resultat['ticket_id'] = ticket_id

        return jsonify(resultat)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)