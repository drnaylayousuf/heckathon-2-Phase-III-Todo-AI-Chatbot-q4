from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool
from sqlalchemy import text
import logging

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_LCGQ75XgEVTw@ep-summer-frog-ah5snk5j-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")

# Global variable to hold the engine
_engine = None

def get_engine():
    """Lazy load the database engine to avoid blocking startup"""
    global _engine
    if _engine is None:
        print("Initializing database engine...")
        from sqlmodel import create_engine

        # Create engine with optimized settings for cloud deployment
        _engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=5,  # Increased pool size for better concurrent handling
            max_overflow=10,  # Allow more overflow connections
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,  # Recycle connections every 5 minutes
            pool_timeout=30,  # Increase timeout for busy connections
            echo=False,  # Disable SQL logging for performance
            connect_args={
                "connect_timeout": 10,  # Increase timeout for slow connections
                "application_name": "hf-fast-app",
                "keepalives_idle": 600,  # Keep idle connections alive
                "keepalives_interval": 30,
                "keepalives_count": 5
            }
        )
        print("Database engine initialized")
    return _engine

# Create session maker - will use the lazy-loaded engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def create_db_and_tables():
    """Create database tables if needed"""
    try:
        print("Creating database tables...")
        engine = get_engine()
        # Ensure all models are imported before creating tables
        from app.models.user import User
        from app.models.task import Task
        from app.models.conversation import Conversation, ConversationMessage
        SQLModel.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        print("Continuing startup...")