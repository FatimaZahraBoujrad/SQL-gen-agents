import requests
import os
from dotenv import load_dotenv
load_dotenv()

OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL")  # e.g. "https://your-url-here"
OPEN_WEBUI_API_KEY = os.getenv("OPEN_WEBUI_API_KEY")

MODEL = "vllm.meta-llama/Llama-3.3-70B-Instruct"

def get_user_intent(message: str) -> str:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {OPEN_WEBUI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    

    prompt = f"""
Tu es un assistant BI intelligent qui aide les utilisateurs à obtenir des informations à partir d'une base de données décisionnelle contenant des indicateurs métiers (KPIs), des données de ventes, clients, produits, etc.

Ton rôle est de comprendre la demande de l’utilisateur afin d’orienter correctement le traitement en aval.

---

## Règles à suivre :

1.  Si la question n’est **pas liée à des données , à l’analyse de KPIs, ou à des requêtes d’extraction de données spécifiques**, réponds par un refus poli.
2.  Si la question concerne **la modification, l’insertion ou la suppression de données** dans la base, refuse catégoriquement — tu es un assistant de lecture uniquement.
3.  Si la question est pertinente mais **incomplète, imprécise ou ambiguë** (période manquante , indicateur flou, vocabulaire trop vague), demande une **clarification concise**.
4. Si la question est pertinente et assez claire ne demande pas des clarifications.
5.  Si la question est claire, valide et orientée lecture (extraction d’un indicateur ou d’une valeur agrégée), résume **en une phrase claire** ce que l’utilisateur cherche à savoir. Cette phrase servira d’entrée pour un agent logique métier.

---

## Format de réponse (obligatoire) :

Réponds strictement avec un objet JSON dans ce format :

{{
  "status": "intent" | "clarification" | "refuse",
  "intent": "résumé structuré de l’objectif de la question (en français clair, sans syntaxe SQL)",
  "user_question": "copie exacte de la question utilisateur",
  "content": "message clair de confirmation, clarification ou refus, sans entrer dans la logique technique"
}}

---

### Exemple :

**Question utilisateur :**  
"Quel est le chiffre d'affaires total par mois pour 2024 ?"

**Réponse attendue :**
{{
  "status": "intent",
  "intent": "Obtenir le chiffre d'affaires total par mois pour l'année 2024",
  "user_question": "Quel est le chiffre d'affaires total par mois pour 2024 ?",
  "content": "D’accord, je note cette demande pour analyse."
}}

---

Maintenant, analyse cette question utilisateur :

'{message}'
"""


    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content":prompt
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }

    response = requests.post(
        f"{OPEN_WEBUI_URL}?bypass_filter=false",
        headers=headers,
        json=payload
    )
    print(response.status_code)
    print(response.text)


    response.raise_for_status()
    
    import json
    raw = response.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
        "status": "clarification",
        "content": "Je n'ai pas compris votre demande. Pouvez-vous la reformuler ?",
        "user_question": message
    }