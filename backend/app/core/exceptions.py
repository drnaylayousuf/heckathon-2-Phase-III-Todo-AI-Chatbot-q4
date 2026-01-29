"""
Custom exceptions and error handlers for the application
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import BaseModel
import logging

# Configure logger
logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    error: str
    message: str
    details: dict = None


class BaseAppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class TaskNotFoundException(BaseAppException):
    """Raised when a task is not found"""
    pass


class UserNotFoundException(BaseAppException):
    """Raised when a user is not found"""
    pass


class UnauthorizedAccessException(BaseAppException):
    """Raised when a user doesn't have access to a resource"""
    pass


class ValidationError(BaseAppException):
    """Raised when validation fails"""
    pass


class DatabaseConnectionException(BaseAppException):
    """Raised when there's a database connection issue"""
    pass


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle validation exceptions"""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation Error",
            "message": "Invalid input data",
            "details": {"errors": str(exc)}
        }
    )


async def http_exception_handler(request: Request, exc) -> JSONResponse:
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error: {exc.detail if hasattr(exc, 'detail') else str(exc)}")
    return JSONResponse(
        status_code=getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={
            "success": False,
            "error": getattr(exc, 'detail', 'Internal Server Error'),
            "message": getattr(exc, 'detail', 'An unexpected error occurred'),
            "details": {}
        }
    )


async def base_app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    """Handle custom application exceptions"""
    logger.error(f"Application error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": type(exc).__name__,
            "message": exc.message,
            "details": exc.details
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions"""
    logger.error(f"General error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "details": {}
        }
    )


def add_exception_handlers(app):
    """Add exception handlers to the FastAPI app"""
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(BaseAppException, base_app_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)