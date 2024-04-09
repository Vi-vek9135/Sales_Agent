from pydantic import BaseModel

class DocumentCreate(BaseModel):
    file_name: str
    file_type: str
    user_id: int

class DocumentResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    user_id: int

    class Config:
        orm_mode = True
