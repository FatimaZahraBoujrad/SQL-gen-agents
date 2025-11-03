from agents.logic_agent import get_business_logic_analysis
from agents.chat_agent import get_user_intent
from api.models import ChatInput,ResponseContext
from rag.retrieval.retriever_functions import format_kpi_docs,format_table_docs
from rag.retrieval.retriever import Retriever
import json
from agents.response_agent import generate_response

def test_logic(input: ChatInput):
    intent = get_user_intent(input.message) # vient du premier agent (chatbot)
    if True:
        retriever = Retriever()

        # 1. Requête pour les KPI (optionnel mais utile)
        kpi_docs = retriever.query(
            query_text=input.message,
            top_k=3,
            where_clause={"doc_type": "kpi_definition"}
        )
        print(kpi_docs)
        # 2. Requête pour les tables (toujours nécessaire)
        table_docs = retriever.query(
            query_text=intent["intent"],
            top_k=6,
            where_clause={"doc_type": "table_schema"}
        )
        kpis_text = format_kpi_docs(kpi_docs)
        tables_text = format_table_docs(table_docs)

        business_task = get_business_logic_analysis(
            intent=intent,
            retrieved_kpis=kpis_text,
            retrieved_tables=tables_text
        )

        print("🎯 Résultat du Business Logic Agent :")
        print(json.dumps(business_task, indent=2, ensure_ascii=False))
        return business_task,intent
    else: 
         return None,intent