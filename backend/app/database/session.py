from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool
from sqlalchemy import text

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_LCGQ75XgEVTw@ep-summer-frog-ah5snk5j-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")

def create_engine_with_postgres_only():
    """Create SQLAlchemy engine with PostgreSQL only - no fallback to SQLite"""
    from sqlmodel import create_engine
    import time

    # Extract and mask the database URL for logging
    db_url_display = DATABASE_URL
    if "://" in db_url_display and "@" in db_url_display:
        protocol, rest = db_url_display.split("://", 1)
        creds, endpoint = rest.split("@", 1)
        if ":" in creds:
            user, pwd = creds.split(":", 1)
            masked_creds = f"{user}:***"
            db_url_display = f"{protocol}://{masked_creds}@{endpoint}"

    print(f"Attempting to connect to PostgreSQL database: {db_url_display}")

    # Retry mechanism for connection
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            engine = create_engine(
                DATABASE_URL,
                poolclass=QueuePool,
                pool_size=2,         # Reduced for Hugging Face free tier
                max_overflow=5,      # Reduced for Hugging Face free tier
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=120,    # Recycle connections more frequently
                pool_timeout=30,     # Add connection timeout
                echo=False,          # Set to True for SQL query logging
                connect_args={
                    "connect_timeout": 15,  # Connection timeout
                    "application_name": "hf-space-todo-app"  # Application name
                }
            )

            # Test the connection
            from sqlalchemy import text
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("Successfully connected to PostgreSQL database!")
                break  # Success, exit retry loop
        except ImportError as e:
            print(f"FATAL ERROR: PostgreSQL driver not available: {e}")
            print("Please ensure psycopg2-binary is installed in your environment.")
            raise
        except ModuleNotFoundError as e:
            if "psycopg2" in str(e):
                print(f"FATAL ERROR: PostgreSQL driver not available: {e}")
                print("Please ensure psycopg2-binary is installed in your environment.")
                raise
            else:
                raise
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:  # Last attempt
                print("Failed to connect to PostgreSQL database after retries")
                print("This is a critical error - application cannot start without database connection.")
                raise
            else:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

    return engine

# Create engine with PostgreSQL only - no fallback
engine = create_engine_with_postgres_only()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def create_db_and_tables():
    """Create database tables on startup - with proper error handling for PostgreSQL"""
    try:
        print("Creating database tables...")
        SQLModel.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # Don't raise here as it might prevent the server from starting
        # Some tables might already exist
        print("Continuing startup (tables may already exist)...")

# For alembic migrations
def get_engine():
    return engine