#!/usr/bin/env python3
"""
Startup script for the Hackathon Todo API
Ensures database tables are created before starting the server
"""

import os
import sys
import time
from app.database.session import create_db_and_tables
from app.config import settings
from app.core.logging_config import get_logger

def main():
    """Initialize the application before starting the server"""
    logger = get_logger(__name__)

    print("Starting Hackathon Todo API initialization...")

    # Create database tables
    print("Creating database tables...")
    try:
        create_db_and_tables()
        print("Database tables created successfully!")
        logger.info("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        logger.error(f"Error creating database tables: {e}")
        # Don't exit here - let the server start anyway

    # Verify important environment variables
    print("Checking environment configuration...")
    if settings.secret_key == "dev-secret-key-for-development-only-change-in-production":
        print("WARNING: Using default secret key. This is insecure for production.")

    if settings.gemini_api_key == "your-gemini-api-key-here":
        print("WARNING: Gemini API key not configured. AI features will be limited.")

    print("Initialization complete. Starting server...")
    logger.info("Application initialization complete")

if __name__ == "__main__":
    main()