#!/usr/bin/env python3
"""
Ultra-minimal server to test basic functionality
"""

import uvicorn
import os
from fastapi import FastAPI

# Create the simplest possible app
app = FastAPI(title="Ultra-Minimal API")

@app.get("/")
def root():
    print("ROOT endpoint called - ultra minimal")
    return {"status": "working", "message": "Ultra-minimal server is running"}

@app.get("/test")
def test():
    print("TEST endpoint called - ultra minimal")
    return {"status": "ok", "message": "Test endpoint is accessible"}

@app.get("/health")
def health():
    print("HEALTH endpoint called - ultra minimal")
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting ultra-minimal server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")