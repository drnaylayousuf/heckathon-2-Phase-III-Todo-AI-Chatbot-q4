#!/usr/bin/env python3
"""
Script to manage users in the database
"""

from app.database.session import SessionLocal
from app.models.user import User
from sqlmodel import select, delete
from app.config import settings

def list_users():
    """List all users in the database"""
    print(f"Database URL: {settings.database_url}")
    print("Listing all users in the database...")

    session = SessionLocal()
    try:
        statement = select(User)
        results = session.exec(statement)
        users = results.all()

        print(f"Found {len(users)} users:")
        for user in users:
            print(f"  - ID: {user.id}, Email: {user.email}, Name: {user.name}, Created: {user.created_at}")

    except Exception as e:
        print(f"Error listing users: {e}")
    finally:
        session.close()

def clear_test_users():
    """Clear all users from the database (for testing purposes)"""
    print("Clearing all users from the database...")

    session = SessionLocal()
    try:
        statement = delete(User)
        result = session.exec(statement)
        session.commit()
        print(f"Cleared all users from database.")
    except Exception as e:
        print(f"Error clearing users: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    print("User Management Script")
    print("1. List users")
    print("2. Clear all users (for testing)")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        list_users()
    elif choice == "2":
        confirm = input("Are you sure you want to clear all users? (y/N): ")
        if confirm.lower() == 'y':
            clear_test_users()
            print("All users cleared. You can now register with the same emails again.")
        else:
            print("Operation cancelled.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()