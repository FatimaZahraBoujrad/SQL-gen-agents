from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import Optional, Any

class ChatInput(BaseModel):
    user_id: str
    message: str

class SQLRequest(BaseModel):
    instruction: str

@dataclass
class ResponseContext:
    status: str
    user_input: str
    intent_content: Optional[str] = None
    kpi_description:Optional[str] = None
    business_reasoning:Optional[str] = None
    sql_query: Optional[str] = None
    sql_result: Optional[Any] = field(default_factory=dict)

