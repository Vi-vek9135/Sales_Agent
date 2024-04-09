# app/utils/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# postgresql+psycopg2://postgres:vivek123@localhost/User
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/my_sales_assistant"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:vivek123@localhost/User"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

















from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# postgresql+psycopg2://postgres:vivek123@localhost/User
# POSTGRES_URL = "postgresql://username:password@localhost:5432/your_database"
POSTGRES_URL = "postgresql+psycopg2://postgres:vivek123@localhost/User"
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()