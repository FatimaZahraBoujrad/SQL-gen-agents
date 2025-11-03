from api.models import ChatInput,ResponseContext
from agents.chat_agent import get_user_intent
from agents.sql_gen_agent import generate_sql
from agents.response_agent import generate_response
from agents.sql_validator import validate_sql_query,execute_safe_sql
from api.business_layer import test_logic
DB_PATH = "entreprise.db"


def flow_orchestrator(input: ChatInput):
    business_task,intent=test_logic(input)

    if business_task!=None and business_task["status"] == "valid" and intent["status"]=="intent":
        sql = generate_sql(business_task)
        print(f"la requete sql est {sql}")
        sql_query = validate_sql_query(sql)
        sql_result = execute_safe_sql(sql_query, DB_PATH)

        context = ResponseContext(
            status="sucess",
            user_input=input.message,
            intent_content=intent["content"],
            kpi_description=business_task["kpi_description"],
            sql_query=sql_query,
            sql_result=sql_result
        )

        response = generate_response(context)
        print(response)
        return response
        """{
                #"message": input.message,
                #"reasoning": business_task["reasoning"],
                #"kpi description":business_task["kpi_description"],
                #"sql": sql,      
                #"resultat sql": sql_result,
                "response": response
            }"""

    else:
        if intent["status"]!="intent":
            context = ResponseContext(
            status=intent["status"],
            user_input=input.message,
            intent_content=intent["content"],           
        )
            response=generate_response(context)
            return response
        context = ResponseContext(
            status=business_task["status"],
            business_reasoning=business_task["reasoning"],
            user_input=input.message,
            intent_content=intent.get("content")
        )
        response = generate_response(context)
        return response
    """{
            #"status":business_task["status"],
            #"message": input.message,
            "response": response
        }"""

    
