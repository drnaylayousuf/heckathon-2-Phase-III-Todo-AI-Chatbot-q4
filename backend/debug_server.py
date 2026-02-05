#!/usr/bin/env python3
"""
Diagnostic server to check what's blocking the application
"""

import uvicorn
import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("=== DIAGNOSTIC SERVER STARTUP ===")
print("Step 1: Import statements completed")

app = FastAPI(title="Diagnostic API")

print("Step 2: App instance created")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Step 3: CORS middleware added")

@app.get("/")
def root_check():
    print("ROOT endpoint accessed at", time.time())
    return {"status": "diagnostic_server_running", "step": 4}

@app.get("/test")
def test_endpoint():
    print("TEST endpoint accessed at", time.time())
    return {"status": "reachable", "step": 5}

@app.get("/health")
def health_check():
    print("HEALTH endpoint accessed at", time.time())
    return {"status": "ok", "step": 6}

print("Step 4: Routes defined - App is ready")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Step 5: Starting server on port {port}")
    print("=== SERVER READY FOR REQUESTS ===")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")