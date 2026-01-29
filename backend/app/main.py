import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth, tasks, chat
from app.database.session import create_db_and_tables
from app.core.security import SecurityHeadersMiddleware
from app.core.rate_limit_middleware import RateLimitMiddleware
from app.core.exceptions import add_exception_handlers
from app.core.logging_config import get_logger
from app.config import settings

# Initialize logger
logger = get_logger(__name__)

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

# Include API routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

# Add exception handlers
add_exception_handlers(app)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hackathon Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}