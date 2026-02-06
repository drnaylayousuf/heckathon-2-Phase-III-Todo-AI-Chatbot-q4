from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool
from sqlalchemy import text
import threading
import time

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

        # Create engine with minimal settings for fastest startup
        _engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=1,
            max_overflow=1,
            pool_pre_ping=False,  # Disabled for faster startup
            pool_recycle=3600,    # Longer recycle
            pool_timeout=5,
            echo=False,
            connect_args={
                "connect_timeout": 5,
                "application_name": "hf-fast-app"
            }
        )
        print("Database engine initialized (will connect on first use)")
    return _engine

def create_db_and_tables():
    """Create database tables - this might run later"""
    try:
        print("Attempting to create database tables...")
        engine = get_engine()
        SQLModel.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Database table creation pending: {e}")
        # This is OK - tables might be created later

# Don't initialize database on startup - let it happen lazily
print("Database setup completed (will connect on demand)")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()