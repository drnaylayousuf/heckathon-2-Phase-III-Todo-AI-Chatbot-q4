import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session
from app.database.session import get_session, engine
from app.core.auth import create_user
from app.schemas.user import UserCreate
from app.models.user import User
from sqlmodel import select

# Test creating a user directly using the same logic as the register endpoint
def test_user_creation():
    print("Testing user creation directly...")

    try:
        # Create a test user data
        test_user_data = UserCreate(
            email="test@example.com",
            password="testpassword123",
            name="Test User"
        )

        print(f"User data: {test_user_data}")

        # Create a database session
        with Session(engine) as session:
            # Check if user already exists
            existing_user = session.query(User).filter(User.email == test_user_data.email).first()
            if existing_user:
                print("User already exists")
                return False

            print("Creating new user...")

            # Create the user
            db_user = create_user(
                session=session,
                email=test_user_data.email,
                password=test_user_data.password,
                name=test_user_data.name
            )

            print(f"User created successfully: {db_user}")
            print(f"User ID: {db_user.id}")
            print(f"User Email: {db_user.email}")
            print(f"Password Hashed: {'*' * len(db_user.password_hash) if db_user.password_hash else 'None'}")

            # Verify the user was saved by querying again
            saved_user = session.query(User).filter(User.email == test_user_data.email).first()
            if saved_user:
                print("Verification: User found in database after creation")
                return True
            else:
                print("Verification: User NOT found in database after creation")
                return False

    except Exception as e:
        print(f"Error during user creation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_user_creation()
    if success:
        print("\n[SUCCESS] Direct user creation test PASSED")
    else:
        print("\n[FAILED] Direct user creation test FAILED")