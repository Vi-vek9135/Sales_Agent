from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# from .base import Base
from ..utils.db import Base
from .user import User

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    file_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"Document(id={self.id}, file_name='{self.file_name}', file_type='{self.file_type}', user_id={self.user_id})"