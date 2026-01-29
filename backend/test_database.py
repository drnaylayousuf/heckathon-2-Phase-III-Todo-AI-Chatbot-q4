from app.database.session import engine
from app.models.user import User
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError

try:
    # Try to connect to the database
    print("Testing database connection...")

    # Try to create tables (this will test the connection)
    from app.database.session import create_db_and_tables
    create_db_and_tables()
    print("[SUCCESS] Database connection successful!")

    # Check if we can query the database
    from sqlmodel import Session
    with Session(engine) as session:
        # Try to count users (should not cause an error even if table is empty)
        statement = select(User)
        users = session.exec(statement).all()
        print(f"[SUCCESS] Successfully queried users table, found {len(users)} users")

except SQLAlchemyError as e:
    print(f"[ERROR] Database connection failed: {e}")
except Exception as e:
    print(f"[ERROR] Error: {e}")