#!/usr/bin/env python3
"""
Final fix for the Hugging Face deployment
Ensures proper request logging and connection handling
"""

import uvicorn
import os
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Configure logging to ensure it works in Hugging Face environment
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create app with enhanced logging
app = FastAPI(
    title=settings.app_name,
    description="API for the Hackathon Todo application with AI-powered chatbot",
    version=settings.app_version,
)

# Add enhanced CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Explicitly allow credentials
    allow_origin_regex=None,
    # Expose headers to the browser
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Content-Type"]
)

# Enhanced request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"[LOG] Incoming request: {request.method} {request.url.path}", flush=True)
    logger.info(f"Incoming request: {request.method} {request.url.path}")

    # Log request headers for debugging
    if 'authorization' in request.headers:
        print("[LOG] Authorization header present", flush=True)
    if 'content-type' in request.headers:
        print(f"[LOG] Content-Type: {request.headers['content-type']}", flush=True)

    response = await call_next(request)

    print(f"[LOG] Response status: {response.status_code} for {request.method} {request.url.path}", flush=True)
    logger.info(f"Response status: {response.status_code} for {request.method} {request.url.path}")

    return response

# Add essential endpoints
@app.get("/")
async def root():
    print("[LOG] Root endpoint accessed", flush=True)
    return {"message": "Backend is running and connected to frontend", "status": "connected", "timestamp": __import__('time').time()}

@app.get("/api/health")
async def api_health():
    print("[LOG] API health endpoint accessed", flush=True)
    return {"status": "healthy", "connected": True, "service": "auth-api"}

@app.get("/test")
async def test_endpoint():
    print("[LOG] Test endpoint accessed", flush=True)
    return {"status": "ok", "message": "Server is receiving requests properly", "connected": True}

# Force immediate startup without database blocking
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"[LOG] Starting server on {host}:{port}", flush=True)
    print(f"[LOG] Allowed origins: {settings.allowed_origins}", flush=True)
    print("[LOG] Server is ready to accept requests", flush=True)

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True,
        reload=False,
        workers=1,
        lifespan="off"  # Disable lifespan to avoid any blocking
    )