"""
Security middleware and utilities
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import re


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security headers to all responses
    """
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        return response


def validate_input(input_str: str, pattern: str = r"^[a-zA-Z0-9\s\-_@.]+$") -> bool:
    """
    Validates input strings against a safe pattern to prevent injection attacks
    """
    if not input_str:
        return True  # Allow empty strings
    return bool(re.match(pattern, input_str))


def sanitize_input(input_str: str) -> str:
    """
    Sanitizes input by removing potentially dangerous characters
    """
    if not input_str:
        return input_str

    # Remove potential SQL injection characters (basic protection)
    dangerous_chars = ["'", "\"", ";", "--", "/*", "*/", "xp_", "sp_"]
    sanitized = input_str
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")

    return sanitized