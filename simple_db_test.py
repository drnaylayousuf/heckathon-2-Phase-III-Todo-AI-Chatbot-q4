#!/usr/bin/env python3
"""
Simple database connectivity test
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

def test_database_connection():
    """Test if we can connect to the database"""
    print("[TEST] Testing database connection...")

    # Get database URL from environment or use default
    database_url = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_LCGQ75XgEVTw@ep-summer-frog-ah5snk5j-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")

    # Mask the password in the URL for display
    display_url = database_url
    if "://" in database_url and "@" in database_url:
        protocol, rest = database_url.split("://", 1)
        creds, endpoint = rest.split("@", 1)
        if ":" in creds:
            user, pwd = creds.split(":", 1)
            display_url = f"{protocol}://{user}:***@{endpoint}"

    print(f"[INFO] Connecting to: {display_url}")

    try:
        # Create engine with reduced settings to avoid blocking
        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=1,
            max_overflow=2,
            pool_pre_ping=True,
            pool_recycle=120,
            pool_timeout=10,
            connect_args={
                "connect_timeout": 10,
                "application_name": "db-test"
            }
        )

        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test_value"))
            row = result.fetchone()
            if row and row.test_value == 1:
                print("[SUCCESS] Database connection successful!")
                print("[SUCCESS] Your application CAN connect to Neon PostgreSQL")

                # Test if we can query existing tables
                try:
                    tables_result = conn.execute(text("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                    """))
                    tables = [row.table_name for row in tables_result.fetchall()]

                    if tables:
                        print(f"[INFO] Found {len(tables)} tables in database:")
                        for table in tables[:10]:  # Show first 10 tables
                            print(f"   - {table}")
                        if len(tables) > 10:
                            print(f"   ... and {len(tables) - 10} more")
                    else:
                        print("[INFO] No tables found in database")

                except Exception as e:
                    print(f"[WARN] Could not query table list: {e}")

                return True
            else:
                print("[ERROR] Database connection test failed - unexpected result")
                return False

    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        print("   This means your data is NOT going to the Neon database")
        return False

def main():
    print("[TEST] Starting Simple Database Test")
    print("=" * 50)

    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print("[INFO] DATABASE_URL environment variable is set")
    else:
        print("[ERROR] DATABASE_URL environment variable is NOT set")
        print("   This is why your data is not going to Neon PostgreSQL")
        print(f"   Current default: postgresql://neondb_owner:npg_LCGQ75XgEVTw@ep-summer-frog-ah5snk5j-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")
        return False

    # Test database connection
    connection_ok = test_database_connection()

    if connection_ok:
        print("\n[SUCCESS] CONCLUSION: Your application CAN connect to Neon PostgreSQL!")
        print("   Data SHOULD be going to your Neon database when the app runs")
        print("   The issue might be with the application startup or specific operations")
    else:
        print("\n[ERROR] CONCLUSION: Your application CANNOT connect to Neon PostgreSQL!")
        print("   Data is NOT going to your Neon database")
        print("   Fix the database connection issues first")

    return connection_ok

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n[TIP] Check your Hugging Face Space environment variables")
        print("    Make sure DATABASE_URL is set with your correct Neon database URL")
        sys.exit(1)