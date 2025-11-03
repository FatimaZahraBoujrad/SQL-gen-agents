from rag.retrieval.retriever import Retriever

retriever = Retriever()
#formatter les docs en text en language naturelle pour la prompt
def format_kpi_docs(kpi_docs): 
    if not kpi_docs["documents"]:
        return "Aucune définition de KPI trouvée."

    summaries = []
    for doc in kpi_docs["documents"][0]:
        summaries.append(doc.strip())
    return "\n\n".join(summaries)


def format_table_docs(table_docs):
    if not table_docs["documents"]:
        return "Aucun schéma de table trouvé."

    summaries = []
    for doc in table_docs["documents"][0]:
        summaries.append(doc.strip())
    return "\n\n".join(summaries)
