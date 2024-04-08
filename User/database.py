from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:vivek123@localhost/User"


# Create a PostgreSQL engine instance
engine = create_engine(DATABASE_URL, echo=True)


# Create declarative base meta instance
Base = declarative_base()


# Create session local class for session maker
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)