from pydantic import BaseModel
from datetime import datetime

class ConversationCreate(BaseModel):
    user_id: int
    query: str
    agent_response: str

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    query: str
    agent_response: str
    timestamp: datetime

    class Config:
        orm_mode = True
