from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Configure engine with connection pooling for Neon
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=False           # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def create_db_and_tables():
    # This function is kept for backward compatibility
    # In production, use alembic migrations instead
    SQLModel.metadata.create_all(bind=engine)

# For alembic migrations
def get_engine():
    return engine