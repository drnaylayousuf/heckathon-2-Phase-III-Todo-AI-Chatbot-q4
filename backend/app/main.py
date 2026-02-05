import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.security import SecurityHeadersMiddleware
from app.core.rate_limit_middleware import RateLimitMiddleware
from app.core.exceptions import add_exception_handlers
from app.core.logging_config import get_logger
from app.config import settings
import threading
import time

# Initialize logger
logger = get_logger(__name__)

def add_request_logging(app: FastAPI):
    """Add middleware to log incoming requests"""
    @app.middleware("http")
    async def log_requests(request, call_next):
        logger.info(f"Request: {request.method} {request.url.path} - START")
        response = await call_next(request)
        logger.info(f"Response: {request.method} {request.url.path} - STATUS {response.status_code}")
        return response

app = FastAPI(
    title=settings.app_name,
    description="API for the Hackathon Todo application with AI-powered chatbot",
    version=settings.app_version,
    debug=settings.debug
)

# Add rate limiting middleware first
app.add_middleware(RateLimitMiddleware)

# Add security middleware second
app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware - configurable for production vs development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    # Additional security headers
    allow_origin_regex=os.getenv("ORIGIN_REGEX"),
    # Expose headers to the browser
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
)

# Add request logging FIRST (before adding routers)
add_request_logging(app)

# Import and add routers AFTER logging middleware
# Delay import to avoid blocking startup
def setup_routers():
    from app.api.routers import auth, tasks, chat
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    app.include_router(chat.router, prefix="/api", tags=["chat"])
    logger.info("Routers initialized successfully")

# Setup routers
setup_routers()

# Add exception handlers
add_exception_handlers(app)

# Database initialization will be done separately to avoid blocking startup
def init_database():
    """Initialize database in a separate thread to avoid blocking startup"""
    try:
        from app.database.session import create_db_and_tables
        print("Initializing database in background thread...")
        create_db_and_tables()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
        import traceback
        traceback.print_exc()

# Start database initialization in a separate thread
db_thread = threading.Thread(target=init_database, daemon=True)
db_thread.start()
print("Database initialization thread started")

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