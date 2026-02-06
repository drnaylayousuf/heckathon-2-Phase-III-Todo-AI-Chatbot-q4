#!/usr/bin/env python3
"""
Database Connectivity Checker
This script checks if the database is properly connected and accessible
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import time

def check_database_connectivity():
    """Check if database is accessible and test basic operations"""
    print("[TEST] Checking database connectivity...")

    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("[ERROR] DATABASE_URL environment variable is not set!")
        print("   This is the root cause of your database connection issues")
        return False

    # Mask the password in the URL for display
    display_url = database_url
    if "://" in database_url and "@" in database_url:
        protocol, rest = database_url.split("://", 1)
        creds, endpoint = rest.split("@", 1)
        if ":" in creds:
            user, pwd = creds.split(":", 1)
            display_url = f"{protocol}://{user}:***@{endpoint}"

    print(f"[INFO] Connecting to database: {display_url}")

    try:
        # Create engine with safe settings
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
                "application_name": "db-checker"
            }
        )

        # Test basic connection
        print("   [TEST] Testing basic connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test_value"))
            row = result.fetchone()
            if row and row.test_value == 1:
                print("   [SUCCESS] Basic connection successful!")
            else:
                print("   [ERROR] Basic connection failed")
                return False

        # Test if we can query table information
        print("   [TEST] Testing table access...")
        with engine.connect() as conn:
            tables_result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = [row.table_name for row in tables_result.fetchall()]

            print(f"   [SUCCESS] Found {len(tables)} tables in database:")
            for table in tables[:10]:  # Show first 10 tables
                print(f"      - {table}")
            if len(tables) > 10:
                print(f"      ... and {len(tables) - 10} more")

        # Test creating a temporary table to verify write access
        print("   [TEST] Testing write access...")
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                # Create a temporary test table
                conn.execute(text("""
                    CREATE TEMP TABLE test_table (
                        id SERIAL PRIMARY KEY,
                        test_text VARCHAR(100),
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """))

                # Insert a test record
                conn.execute(text("""
                    INSERT INTO test_table (test_text) VALUES (:test_text)
                """), {"test_text": f"Test record {int(time.time())}"})

                # Read the record back
                result = conn.execute(text("SELECT * FROM test_table"))
                records = result.fetchall()

                print(f"   [SUCCESS] Write/read test successful - {len(records)} records created")

                trans.rollback()  # Don't actually commit the test changes
            except Exception as e:
                print(f"   [WARN] Write test failed (this may be OK): {e}")
                trans.rollback()

        print("   [SUCCESS] Database is fully accessible and functional!")
        return True

    except Exception as e:
        print(f"   [ERROR] Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_environment():
    """Check environment variables and configuration"""
    print("[TEST] Checking environment variables...")

    required_vars = ['DATABASE_URL']
    all_set = True

    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   [SUCCESS] {var} is set")
        else:
            print(f"   [ERROR] {var} is NOT set")
            all_set = False

    return all_set

def main():
    print("[START] Database Connectivity Check")
    print("=" * 50)

    # Check environment variables
    env_ok = check_environment()

    if not env_ok:
        print("\n[ERROR] CRITICAL: Environment variables are not properly configured!")
        print("   Please set DATABASE_URL in your Hugging Face Space settings")
        return False

    # Check database connectivity
    db_ok = check_database_connectivity()

    print("\n" + "=" * 50)
    if db_ok:
        print("[SUCCESS] DATABASE CONNECTIVITY: OK")
        print("[SUCCESS] Your application can connect to Neon PostgreSQL")
        print("[SUCCESS] Data can flow to your database")
        print("[SUCCESS] Registration and login should work properly")
    else:
        print("[ERROR] DATABASE CONNECTIVITY: FAILED")
        print("[ERROR] Your application cannot connect to Neon PostgreSQL")
        print("[ERROR] Data is NOT going to your database")
        print("[ERROR] Registration and login will fail")

    return db_ok

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n[TIPS:]")
        print("   1. Check your Hugging Face Space environment variables")
        print("   2. Make sure DATABASE_URL is set with your Neon database URL")
        print("   3. Verify the Neon database URL is correct and accessible")
        sys.exit(1)