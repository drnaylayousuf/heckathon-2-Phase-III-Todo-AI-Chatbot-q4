#!/usr/bin/env python3
"""
Database connectivity and data insertion test script
"""

import os
import sys
import asyncio
from sqlmodel import Session, select
from sqlalchemy import text
from datetime import datetime

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.session import get_engine, get_session
from backend.app.models.user import User, UserCreate
from backend.app.core.auth import get_password_hash, create_user

def test_database_connection():
    """Test if we can connect to the database"""
    print("🔍 Testing database connection...")

    try:
        engine = get_engine()

        # Test basic connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row:
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database connection failed - no result returned")
                return False

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_insertion():
    """Test if we can insert and retrieve data"""
    print("\n🔍 Testing data insertion...")

    try:
        # Create a test user
        test_email = f"test_{int(datetime.now().timestamp())}@example.com"
        test_password = "testpassword123"
        test_name = "Test User"

        print(f"📝 Creating test user: {test_email}")

        # Use the session to create a user
        with next(get_session()) as session:
            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == test_email)).first()
            if existing_user:
                print(f"⚠️  User {test_email} already exists, skipping creation")
                return True

            # Create new user using the auth function
            hashed_password = get_password_hash(test_password)
            db_user = User(
                email=test_email,
                password_hash=hashed_password,
                name=test_name
            )

            session.add(db_user)
            session.commit()
            session.refresh(db_user)

            print(f"✅ User created successfully with ID: {db_user.id}")

            # Now try to retrieve the user
            retrieved_user = session.exec(select(User).where(User.email == test_email)).first()
            if retrieved_user:
                print(f"✅ User retrieved successfully from database!")
                print(f"   Email: {retrieved_user.email}")
                print(f"   Name: {retrieved_user.name}")
                print(f"   ID: {retrieved_user.id}")
                print(f"   Created: {retrieved_user.created_at}")

                # Clean up - delete the test user
                session.delete(retrieved_user)
                session.commit()
                print(f"🗑️  Test user cleaned up successfully")

                return True
            else:
                print("❌ Failed to retrieve the user from database")
                return False

    except Exception as e:
        print(f"❌ Data insertion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        print("✅ DATABASE_URL is set")
        # Mask the password in the URL for safety
        if "@" in database_url and ":" in database_url.split("@")[0]:
            user_pass = database_url.split("@")[0].split("://")[1]
            if ":" in user_pass:
                user, pwd = user_pass.split(":", 1)
                masked_url = database_url.replace(f"{user}:{pwd}", f"{user}:***")
                print(f"   Database URL: {masked_url}")
        else:
            print(f"   Database URL: {database_url}")
    else:
        print("❌ DATABASE_URL is not set!")
        print("   This is likely the reason your data isn't going to the database")
        return False

    return True

def main():
    print("🚀 Starting Database Connectivity Test")
    print("=" * 50)

    # Check environment variables
    env_ok = check_environment_variables()
    if not env_ok:
        print("\n❌ CRITICAL: Environment variables are not properly configured!")
        print("   Make sure DATABASE_URL is set in your Hugging Face Space settings")
        return False

    # Test database connection
    connection_ok = test_database_connection()
    if not connection_ok:
        print("\n❌ CRITICAL: Cannot connect to the database!")
        print("   Check your DATABASE_URL and network connectivity")
        return False

    # Test data insertion
    data_ok = test_data_insertion()
    if not data_ok:
        print("\n❌ CRITICAL: Cannot insert/retrieve data from the database!")
        return False

    print("\n🎉 All tests passed!")
    print("✅ Your application can connect to Neon PostgreSQL")
    print("✅ Your application can insert and retrieve data")
    print("✅ Data is going to your Neon database successfully!")

    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ CONCLUSION: Your data is going to the Neon PostgreSQL database!")
    else:
        print("\n❌ CONCLUSION: There are issues with database connectivity!")
        sys.exit(1)