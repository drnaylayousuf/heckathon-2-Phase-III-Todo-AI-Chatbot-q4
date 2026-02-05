#!/usr/bin/env python3
"""
Diagnostic server to check what's happening with the API
"""

import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import traceback

# Create a minimal app to test
app = FastAPI(title="Diagnostic API")

@app.get("/")
def root_check():
    return {"status": "diagnostic_server_running", "timestamp": str(__import__('datetime').datetime.now())}

@app.get("/test")
def test_endpoint():
    return {"status": "reachable", "message": "This endpoint is accessible"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "diagnostic"}

@app.get("/routes")
def list_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods)
            })
    return {"routes": routes}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting diagnostic server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")