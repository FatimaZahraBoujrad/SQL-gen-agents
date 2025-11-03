from fastapi import APIRouter
#from agents.chat_agent import get_user_intent
#from agents.sql_gen_agent import generate_sql
#from agents.response_agent import generate_response
from api.orchestration import flow_orchestrator
from api.models import ChatInput
#from api.business_layer import test_logic
from agents_v2.kpi_agent import ask_kpi_agent
router = APIRouter()

@router.post("/chat-powerbi") #endpoint qui utlise les kpis ectraites depuis les rapports powerbi
def chat(input: ChatInput):
    return ask_kpi_agent(input.message)
   
    
