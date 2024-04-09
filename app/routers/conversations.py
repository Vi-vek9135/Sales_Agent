# app/routers/conversations.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.conversation import Conversation
from schemas.conversation import ConversationCreate, ConversationResponse
from utils.db import get_db
from utils.security import get_current_user
from utils.agent import get_agent_response
from models.user import User

# from ..utils.agent import handle_user_query





router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)

@router.post("/", response_model=ConversationResponse)
def start_conversation(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    agent_response = get_agent_response(query)
    conversation = ConversationCreate(
        user_id=current_user.id,
        agent_response=agent_response,
    )
    db_conversation = Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return ConversationResponse.from_orm(db_conversation)

@router.get("/", response_model=list[ConversationResponse])
def get_conversation_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    db_conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .all()
    )
    return [ConversationResponse.from_orm(c) for c in db_conversations]













router = APIRouter()

@router.post("/")
def chat_with_agent(query: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Handle the user's query using the agent
    agent_response = get_agent_response(query)

    # Save the conversation to the database
    conversation = Conversation(user_id=user.id, query=query, agent_response=agent_response)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {"response": agent_response}




@router.get("/history")
def get_conversation_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    conversations = db.query(Conversation).filter(Conversation.user_id == current_user.id).all()
    return [
        {
            "id": conversation.id,
            "query": conversation.query,
            "agent_response": conversation.agent_response,
            "timestamp": conversation.timestamp
        }
        for conversation in conversations
    ]
