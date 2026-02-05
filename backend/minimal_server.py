#!/usr/bin/env python3
"""
Minimal server for testing basic functionality
"""

import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("Creating minimal app...")

app = FastAPI(title="Minimal Test API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    print("Root endpoint called")
    return {"status": "working", "message": "Minimal server is running"}

@app.get("/test")
def test():
    print("Test endpoint called")
    return {"status": "ok", "message": "Test endpoint is accessible"}

@app.get("/api/health")
def api_health():
    print("API health endpoint called")
    return {"status": "healthy"}

@app.post("/api/register")
async def register_test():
    print("Register endpoint called")
    return {"message": "Register endpoint is accessible"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting minimal server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")