"""
Application configuration management
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Database settings
    database_url: str = Field(default="postgresql://neondb_owner:npg_LCGQ75XgEVTw@ep-summer-frog-ah5snk5j-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require", alias="DATABASE_URL")
    db_pool_size: int = 20
    db_pool_overflow: int = 10

    # Security settings
    secret_key: str = "dev-secret-key-for-development-only-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS settings - Use the origins from environment variable
    allowed_origins_str: str = Field(default="http://localhost:3000,http://127.0.0.1:3000,https://heckathon-2-phase-iii-todo-ai-chatb.vercel.app,https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space", alias="ALLOWED_ORIGINS")

    @property
    def allowed_origins(self) -> List[str]:
        """Convert the comma-separated string to a list of origins."""
        return [origin.strip() for origin in self.allowed_origins_str.split(",")]

    # Rate limiting
    rate_limit_max: int = 100
    rate_limit_window: int = 3600  # in seconds

    # Logging
    log_level: str = "INFO"
    log_file: str = "app.log"

    # Application
    app_name: str = "Hackathon Todo API"
    app_version: str = "1.0.0"
    debug: bool = False

    # AI Configuration
    gemini_api_key: str = Field(default="your-gemini-api-key-here", alias="GEMINI_API_KEY")
    default_ai_model: str = Field(default="gemini-1.5-flash", alias="DEFAULT_AI_MODEL")
    ai_temperature: float = Field(default=0.7, alias="AI_TEMPERATURE")
    ai_max_tokens: int = Field(default=1024, alias="AI_MAX_TOKENS")
    chatbot_name: str = Field(default="Todo Assistant", alias="CHATBOT_NAME")
    chatbot_personality: str = Field(default="You are a helpful AI assistant that helps users manage their tasks and todos through natural language.", alias="CHATBOT_PERSONALITY")

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow",  # Allow extra env vars to be loaded
        "env_nested_delimiter": "__"  # For nested configs if needed
    }


# Create a global settings instance
settings = Settings()