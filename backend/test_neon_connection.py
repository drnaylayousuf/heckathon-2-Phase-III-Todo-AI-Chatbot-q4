#!/usr/bin/env python3
"""
Test script to verify connection to Neon database
"""

from app.database.session import engine
from app.models.user import User
from sqlmodel import select
from app.config import settings

def test_connection():
    print(f"Database URL: {settings.database_url}")
    print("Testing database connection...")

    try:
        # Attempt to connect and run a simple query
        with engine.connect() as conn:
            print("✓ Successfully connected to database!")

            # Test if tables exist by trying to inspect them
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Tables in database: {tables}")

            # Try to query users table if it exists
            if 'user' in tables or 'users' in tables:
                from app.database.session import SessionLocal
                session = SessionLocal()
                try:
                    # Count existing users
                    statement = select(User)
                    results = session.exec(statement)
                    users = results.all()
                    print(f"Found {len(users)} users in the database")

                    if users:
                        print("Sample user data:")
                        for user in users[:2]:  # Show first 2 users
                            print(f"  - ID: {user.id}, Email: {user.email}, Name: {user.name}")
                finally:
                    session.close()

    except Exception as e:
        print(f"✗ Error connecting to database: {e}")

if __name__ == "__main__":
    test_connection()