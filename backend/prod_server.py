#!/usr/bin/env python3
"""
Production server runner for the Hackathon Todo API
Compatible with deployment platforms like Hugging Face Spaces, Render, etc.
"""

import uvicorn
import os
import sys
import signal
import time
from app.config import settings


def signal_handler(sig, frame):
    """Handle graceful shutdown"""
    print("\nReceived interrupt signal. Shutting down gracefully...")
    sys.exit(0)


def main():
    """Run the production server"""
    print(f"Starting Hackathon Todo API server...")
    print(f"App: {settings.app_name} v{settings.app_version}")
    print(f"Debug mode: {settings.debug}")

    # Log database URL but hide sensitive parts
    db_url = settings.database_url
    if "://" in db_url:
        protocol, rest = db_url.split("://", 1)
        if "@" in rest:
            creds, endpoint = rest.split("@", 1)
            if ":" in creds:
                user, pwd = creds.split(":", 1)
                masked_creds = f"{user}:***"
                db_url = f"{protocol}://{masked_creds}@{endpoint}"
    print(f"Database: {db_url}")

    # Import and initialize database here to catch any database errors early
    try:
        from app.database.session import engine
        print("Database engine initialized successfully")

        # Test database connection
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection test successful!")

    except Exception as e:
        print(f"FATAL: Database connection failed: {e}")
        raise

    # Use PORT environment variable if available (for Heroku, Hugging Face, etc.)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")  # Bind to all interfaces for cloud deployment

    print(f"Serving on {host}:{port}")
    print("-" * 50)

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info",
            timeout_keep_alive=300,  # Increase keep-alive timeout for slow connections
            timeout_graceful_shutdown=10,  # Graceful shutdown timeout
            workers=1,  # Use single worker for Hugging Face compatibility
            lifespan="on"  # Enable lifespan events
        )
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()