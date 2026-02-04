from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

def create_engine_with_fallback():
    """Create SQLAlchemy engine with fallback to SQLite if PostgreSQL driver is not available"""
    try:
        from sqlmodel import create_engine
        # Try to create engine with the configured database URL
        return create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,    # Recycle connections every 5 minutes
            echo=False           # Set to True for SQL query logging
        )
    except ImportError as e:
        # If PostgreSQL driver is not available, fall back to SQLite
        if "psycopg2" in str(e) or "psycopg" in str(e):
            print(f"PostgreSQL driver not available: {e}. Falling back to SQLite.")
            fallback_url = "sqlite:///./todo_app.db"
            print(f"Using fallback database: {fallback_url}")

            from sqlmodel import create_engine
            return create_engine(
                fallback_url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False
            )
        else:
            # Re-raise if it's a different import error
            raise

# Create engine with fallback mechanism
engine = create_engine_with_fallback()

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