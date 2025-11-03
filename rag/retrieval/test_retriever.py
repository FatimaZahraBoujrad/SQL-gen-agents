from retriever import Retriever

retriever = Retriever()

question = "le nbr de commandes  ?"
filtre = {"report": "Change Order"}

# Requête vers la base vectorielle
resultats = retriever.query(query_text=question, top_k=3)

# Affichage
print("\n🔎 Résultats de la recherche :\n")
for i, r in enumerate(resultats):
    print(f"Résultat {i+1}")
    print("Contenu du document :\n", r['text'])
    print("Métadonnées :", r['metadata'])
    print()
