#!/usr/bin/env python3
"""
Production server runner for the Hackathon Todo API
Compatible with deployment platforms like Hugging Face Spaces, Render, etc.
"""

import uvicorn
import os
from app.config import settings


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

    # Use PORT environment variable if available (for Heroku, Hugging Face, etc.)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")  # Bind to all interfaces for cloud deployment

    print(f"Serving on {host}:{port}")
    print("-" * 50)

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )


if __name__ == "__main__":
    main()