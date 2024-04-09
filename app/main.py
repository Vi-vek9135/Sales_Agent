from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, documents, conversations
from .utils.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(conversations.router, prefix="/conversations", tags=["conversations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sales Assistant API"}