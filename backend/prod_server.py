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

    # Defer database initialization to application startup event
    print("Deferring database initialization to app startup...")

    # Use PORT environment variable if available (for Heroku, Hugging Face, etc.)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")  # Bind to all interfaces for cloud deployment

    print(f"Serving on {host}:{port}")
    print("-" * 50)
    print("Server is now ready to accept requests...")

    # Run uvicorn server - this should block and keep the process alive indefinitely
    # The server will run until manually stopped
    import sys
    try:
        # Configure for Hugging Face Spaces with proper logging
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info",  # Changed from debug to info for cleaner logs
            access_log=True,  # Enable access logging to see requests
            timeout_keep_alive=300,  # Increase keep-alive timeout for slow connections
            workers=1,  # Use single worker for Hugging Face compatibility
            lifespan="on",  # Enable lifespan events
            proxy_headers=True,  # Enable proxy headers for cloud deployments
            forwarded_allow_ips="*",  # Allow forwarded IPs for cloud deployments
            server_header=False,  # Hide server header for security
            date_header=False,  # Hide date header for security
        )
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Server process ending...")
        # Don't exit the process - let the platform manage it
        import time
        # Keep process alive briefly to allow proper cleanup
        time.sleep(1)


if __name__ == "__main__":
    main()