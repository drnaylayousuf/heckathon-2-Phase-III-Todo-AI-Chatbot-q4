"""
Rate limiting middleware for the application
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.rate_limiter import check_rate_limit
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware that applies rate limits to all requests
    """
    async def dispatch(self, request: Request, call_next):
        # Extract client IP address for rate limiting
        client_ip = request.client.host

        # Check rate limit
        is_allowed, retry_after = check_rate_limit(
            identifier=client_ip,
            max_requests=100,  # Default: 100 requests per hour
            window=3600        # Default: 1 hour window
        )

        if not is_allowed:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return Response(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": str(int(retry_after))}
            )

        response = await call_next(request)
        return response