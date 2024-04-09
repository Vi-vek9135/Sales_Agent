from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
# from .base import Base
from utils.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    documents = relationship("Document", back_populates="owner")

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"
