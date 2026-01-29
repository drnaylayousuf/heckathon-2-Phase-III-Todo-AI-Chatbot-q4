#!/usr/bin/env python3
"""
Development server runner for the Hackathon Todo API
"""

import uvicorn
import os
from app.config import settings


def main():
    """Run the development server"""
    print(f"Starting Hackathon Todo API server...")
    print(f"App: {settings.app_name} v{settings.app_version}")
    print(f"Debug mode: {settings.debug}")
    print(f"Database: {settings.database_url}")
    print("-" * 50)

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )


if __name__ == "__main__":
    main()