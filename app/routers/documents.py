# app/routers/documents.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse
from app.utils.db import get_db
from app.models.user import User
from app.utils.security import get_current_user

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
from app.models.document import Document
from app.models.user import User  # Import the User model
from app.schemas.document import DocumentCreate, DocumentResponse
from app.utils.db import get_db
from app.utils.security import get_current_user

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














# from fastapi import APIRouter, Depends, File, UploadFile
# from ..models.document import Document
# from ..utils.db import get_db
# from sqlalchemy.orm import Session
# from ..utils.security import get_current_user

# router = APIRouter()

# @router.post("/upload")
# def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     # Save the file to storage (e.g., S3, local file system)
#     # Create a new Document instance and save it to the database
#     pass

# @router.get("/")
# def list_documents(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     # Retrieve the documents for the current user
#     pass