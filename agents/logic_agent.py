import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL")  # e.g. "http://localhost:3000"
OPEN_WEBUI_API_KEY = os.getenv("OPEN_WEBUI_API_KEY")

MODEL = "vllm.meta-llama/Llama-3.3-70B-Instruct"


def get_business_logic_analysis(intent, retrieved_kpis: str, retrieved_tables: str) -> dict:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {OPEN_WEBUI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prompt business logic (from our previous design)
    prompt = f"""
Tu es un expert métier et analyste BI. Ton objectif est d'analyser une question en langage naturel et de déterminer si elle peut être traduite en une requête SQL valide à l’aide :

- Des définitions d’indicateurs (KPIs)
- Du schéma des tables (colonnes et descriptions)

---

### 📘 Données disponibles :

**Définitions de KPI** :
{retrieved_kpis}

**Schéma des tables** :
{retrieved_tables}

---

### 📥 Question de l'utilisateur :

{intent}

---
---

## Règles à suivre :

1.  Si la question n’est **pas liée à des données , à l’analyse de KPIs, ou à des requêtes d’extraction de données spécifiques**, réponds par un refus poli.
2.  Si la question concerne **la modification, l’insertion ou la suppression de données** dans la base, refuse catégoriquement — tu es un assistant de lecture uniquement.
3.  Si la question est pertinente mais **incomplète, imprécise ou ambiguë** (période manquante , indicateur flou, vocabulaire trop vague), demande une **clarification concise**.
4. Si la question est pertinente et assez claire ne demande pas des clarifications.
5.  Si la question est claire, valide et orientée lecture (extraction d’un indicateur ou d’une valeur agrégée), résume **en une phrase claire** ce que l’utilisateur cherche à savoir. Cette phrase servira d’entrée pour un agent logique métier.

---

### 🎯 Instructions (raisonne étape par étape) :

1. Détermine si la question concerne un KPI défini ou une demande ad hoc.
2. Si c’est un KPI, identifie lequel et pourquoi.
3. Identifie les tables pertinentes et nécessaires.
4. Repère les colonnes nécessaires (même si implicites).
5. Déduis les jointures nécessaires entre tables.
6. Repère les filtres implicites (périodes, conditions).
7. Identifie les agrégations (somme, moyenne,etc.).
8. Si la question est invalide ou hors domaine, refuse avec une explication.
 
---

### 🧾 Format de sortie (JSON obligatoire) :

{{
  "status": "valid" | "refusal" | "clarification",
  "question_type": "kpi" | "adhoc" | null,
  "kpi": "..." | null,
  "formule de calcul": "formule de calcul de kpi si connue"|null,
  "kpi_description":"description de la kpi dans retrieved_kpis telle quelle est si c'est une kpi"|null
  "user_question":"la question telle quelle est",
  "reasoning": "...",
  "tables": [
    {{
      "name": "...",
      "columns_used": ["..."]
    }}
  ],
  "joins": [
    {{
      "left_table": "...",
      "left_column": "...",
      "right_table": "...",
      "right_column": "..."
    }}
  ],
  "filters": [
    {{
      "column": "...",
      "operator": "...",
      "value": "..."
    }}
  ],
  "aggregation": {{
    "type": "...",
    "column": "..."
  }} | null,
  "output_format": "value_only" | "table" | "time_series" | "percentage"
}}

---

Ne génère **aucune requête SQL**. Ton rôle est uniquement de préparer les éléments métier nécessaires à la génération.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt}
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

    raw = response.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "status": "refusal",
            "question_type": None,
            "kpi": None,
            "reasoning": "La sortie du modèle n'était pas un JSON valide.",
            "tables": [],
            "joins": [],
            "filters": [],
            "aggregation": None,
            "output_format": "value_only"
        }
