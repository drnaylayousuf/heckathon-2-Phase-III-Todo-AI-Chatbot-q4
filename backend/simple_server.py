#!/usr/bin/env python3
"""
Simple server runner optimized for Hugging Face Spaces
"""

import uvicorn
import os
from app.config import settings

def main():
    """Run the server with Hugging Face optimized settings"""
    print("Starting Hackathon Todo API server for Hugging Face...")
    print(f"App: {settings.app_name} v{settings.app_version}")

    # Log database URL
    db_url = settings.database_url
    print(f"Database URL configured: {'Yes' if db_url else 'No'}")

    # Test import of main app to catch issues early
    try:
        from app.main import app
        print("✓ Application imported successfully")
    except Exception as e:
        print(f"✗ Application import failed: {e}")
        raise

    # Test database connection
    try:
        from app.database.session import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        raise

    # Use the port that Hugging Face provides
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"

    print(f"Starting server on {host}:{port}")
    print("Server is ready to accept requests...")

    # Run with minimal configuration for Hugging Face
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level="info",
        access_log=True,  # Enable access logging
        reload=False,
        workers=1
    )

if __name__ == "__main__":
    main()