# app/routers/documents.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from models.document import Document
from schemas.document import DocumentCreate, DocumentResponse
from utils.db import get_db
from models.user import User
from utils.security import get_current_user

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@router.post("/", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = DocumentCreate(
        file_name=file.filename,
        file_type=file.content_type,
        user_id=current_user.id,
    )
    db_document = Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Save the file to cloud storage or file system
    # ...

    return DocumentResponse.from_orm(db_document)








from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from models.document import Document
from models.user import User  # Import the User model
from schemas.document import DocumentCreate, DocumentResponse
from utils.db import get_db
from utils.security import get_current_user

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@router.post("/", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = DocumentCreate(
        file_name=file.filename,
        file_type=file.content_type,
        user_id=current_user.id,
    )
    db_document = Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    # Save the file to cloud storage or file system
    # ...
    return DocumentResponse.from_orm(db_document)

@router.get("/")
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Retrieve the documents for the current user
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return [DocumentResponse.from_orm(doc) for doc in documents]













