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
    print(f"Log level: {settings.log_level}")
    print(f"Log file: {settings.log_file}")

    # Initialize database tables
    from app.database.session import create_db_and_tables
    create_db_and_tables()

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
    port = int(os.environ.get("PORT", 7860))  # Hugging Face typically uses 7860
    host = os.environ.get("HOST", "0.0.0.0")  # Bind to all interfaces for cloud deployment

    print(f"Serving on {host}:{port}")
    print("-" * 50)
    print("Server is now ready to accept requests...")

    # Run uvicorn server - this should block and keep the process alive indefinitely
    import sys
    try:
        # Configure for Hugging Face Spaces with proper logging
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info",  # Cleaner logs
            access_log=True,  # Enable access logging
            timeout_keep_alive=300,  # Keep-alive timeout
            workers=1,  # Single worker for Hugging Face compatibility
            lifespan="on",  # Enable lifespan events
            proxy_headers=True,  # Proxy headers for cloud deployments
            forwarded_allow_ips="*",  # Allow forwarded IPs
            server_header=False,  # Hide server header for security
            date_header=False,  # Don't send date header
        )
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Server process ending...")
        import time
        # Keep process alive briefly to allow proper cleanup
        time.sleep(1)


if __name__ == "__main__":
    main()