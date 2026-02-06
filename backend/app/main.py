import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import get_logger
from app.config import settings
from app.database.session import create_db_and_tables
import asyncio

# Initialize logger
logger = get_logger(__name__)

# Create the app instance
app = FastAPI(
    title=settings.app_name,
    description="API for the Hackathon Todo application with AI-powered chatbot",
    version=settings.app_version,
    debug=settings.debug
)

# Add startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup initiated")
    # Create database tables
    create_db_and_tables()
    logger.info("Application startup complete")
    logger.info(f"Allowed origins: {settings.allowed_origins}")

# CORS middleware - configurable for production vs development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url.path} from {request.client.host} - START")
    response = await call_next(request)
    logger.info(f"Response: {request.method} {request.url.path} - STATUS {response.status_code}")
    return response

# Import routers safely after initialization
try:
    from app.api.routers import auth, tasks, chat
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    app.include_router(chat.router, prefix="/api", tags=["chat"])
    logger.info("Routers loaded successfully")
except Exception as e:
    logger.error(f"Error loading routers: {e}")
    # Continue without routers so the app can still start

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Hackathon Todo API", "status": "running"}

@app.get("/api/health")
def api_health_check():
    logger.info("API health endpoint accessed")
    return {"status": "healthy", "service": "auth-api"}

@app.get("/test")
def test_endpoint():
    logger.info("Test endpoint accessed")
    return {"status": "ok", "message": "Server is receiving requests"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Health check for Hugging Face
@app.get("/status/ready")
def readiness_check():
    return {"status": "ready"}

@app.get("/status/alive")
def liveness_check():
    return {"status": "alive"}