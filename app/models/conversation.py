from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
# from .base import Base
from utils.db import Base
from .user import User

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query = Column(String)
    agent_response = Column(String)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="conversations")

    def __repr__(self):
        return f"Conversation(id={self.id}, user_id={self.user_id}, query='{self.query}', agent_response='{self.agent_response}', timestamp='{self.timestamp}')"
