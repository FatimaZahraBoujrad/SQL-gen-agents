import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()
OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL")  
OPEN_WEBUI_API_KEY = os.getenv("OPEN_WEBUI_API_KEY")
MODEL = "vllm.meta-llama/Llama-3.3-70B-Instruct"

def generate_sql(logic_json) -> str:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {OPEN_WEBUI_API_KEY}",
        "Content-Type": "application/json"
    }
    logic_json_example = {
  "tables": [
    { 
      "name": "ventes",
      "columns_used": ["id_client", "id_vente"]
    },
    { 
      "name": "clients",
      "columns_used": ["id"]
    }
  ],
  "joins": [
    {
      "left_table": "ventes",
      "left_column": "id_client",
      "right_table": "clients",
      "right_column": "id"
    }
  ],
  "filters": [],
  "aggregation": {
    "type": "count",
    "column": "id_client"
  },
  "output": "value_only"
}


    prompt = f"""
    Tu es un assistant expert en SQL spécialisé dans les bases de données **SQLite** et l’analyse de données métier.

Ta tâche est de **générer une requête SQL précise et exécutable** à partir d’un JSON de logique métier structuré. Tu dois te baser **strictement** sur les données et contraintes fournies. **Aucune supposition n’est autorisée.**

---

### Entrée : JSON de logique métier

```json
{json.dumps(logic_json, indent=2)}
Instructions de génération :
 Tables et colonnes :
N’utilise que les noms de tables et colonnes présents dans tables[].name et tables[].columns_used.

 Jointures :
Applique uniquement les jointures indiquées dans joins[] via JOIN explicite (ON table.col = table.col).

Filtres :
Ajoute les filters[] dans une clause WHERE.

Respecte la syntaxe : col operator value.

Si le filtre utilise une valeur dynamique comme "cette année", remplace par une comparaison explicite avec strftime('%Y', ...) = '2025'.

 Agrégation :
Si aggregation est présente :

Utilise la fonction SQL correspondante (SUM, AVG, COUNT, etc.)

Applique-la sur aggregation.column (si cette colonne est bien listée dans columns_used)

Donne un alias clair (AS ...)

 Format de sortie :
"time_series" → Ajoute GROUP BY strftime('%Y-%m', <date_column>), et ORDER BY par mois.

"table" → GROUP BY sur les colonnes non agrégées.

"value_only" → Requête simple avec ou sans agrégation. Pas de GROUP BY.

 Style :
Pas de SELECT *

Utilise des alias de table (v, c, etc.) pour améliorer la lisibilité

Pas d’indentation excessive

Un seul bloc SQL bien formé

Ne fais jamais :
 -Ne crée pas de jointure implicite.

 -N’invente aucun nom de table ou de colonne.

 -N’utilise pas de fonctions non compatibles SQLite.

 -N’ajoute aucun texte explicatif après la requête.

Format de sortie :
Commence par un commentaire décrivant le contexte métier (en français), puis écris la requête SQL sans aucune explication supplémentaire.

Exemple de sortie correcte :


-- Requête SQL pour analyser le revenu mensuel en 2023
SELECT
  strftime('%Y-%m', fact_ventes.date_vente) AS mois,
  SUM(fact_ventes.montant) AS revenu_total
FROM fact_ventes
WHERE fact_ventes.date_vente >= '2023-01-01'
  AND fact_ventes.date_vente <= '2023-12-31'
GROUP BY mois
ORDER BY mois;

### Exemples :


Exemple  – Taux de réachat
{json.dumps(logic_json_example, indent=2)}

-- Requête SQL pour calculer le taux de réachat (clients ayant acheté plus d'une fois / total clients)
SELECT
  CAST(COUNT(DISTINCT v.id_client) FILTER (WHERE achats > 1) AS FLOAT) / COUNT(*) AS taux_reachat
FROM (
  SELECT v.id_client, COUNT(*) AS achats
  FROM ventes v
  GROUP BY v.id_client
) sous_requete

"""


    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
           
        ]
    }

    response = requests.post(
        f"{OPEN_WEBUI_URL}?bypass_filter=false",
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


