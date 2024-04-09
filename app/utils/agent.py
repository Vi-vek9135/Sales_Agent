from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from ..models.conversation import Conversation
from ..utils.db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

# Initialize the language model
llm = OpenAI(temperature=0.7, model_name="text-davinci-003")

# Initialize the conversation memory
memory = ConversationBufferMemory(return_messages=True)

# Initialize the conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

def get_agent_response(query: str, user_id: int, db: Session = Depends(get_db)):
    # Get the conversation history for the user
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
    for conversation in conversations:
        memory.chat_memory.add_user_message(conversation.query)
        memory.chat_memory.add_agent_message(conversation.agent_response)

    # Generate the agent's response
    agent_response = conversation.generate_response(query)

    # Save the new conversation entry
    new_conversation = Conversation(
        user_id=user_id,
        query=query,
        agent_response=agent_response
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return agent_response