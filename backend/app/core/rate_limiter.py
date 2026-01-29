"""
Rate limiting functionality for the application
"""
import time
from typing import Dict, Tuple
from collections import defaultdict
import threading


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter for development/testing
    For production, consider using Redis-based rate limiter
    """
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, identifier: str, max_requests: int, window: int) -> Tuple[bool, float]:
        """
        Check if a request is allowed based on rate limiting rules

        Args:
            identifier: Unique identifier for the client (e.g., IP address, user ID)
            max_requests: Maximum number of requests allowed
            window: Time window in seconds

        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        current_time = time.time()

        with self.lock:
            # Clean old requests outside the window
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if current_time - req_time < window
            ]

            # Check if we're under the limit
            if len(self.requests[identifier]) < max_requests:
                # Add current request
                self.requests[identifier].append(current_time)
                return True, 0.0

            # Calculate when the oldest request will expire
            oldest_request = self.requests[identifier][0]
            retry_after = window - (current_time - oldest_request)

            return False, max(0.0, retry_after)


# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()


def check_rate_limit(identifier: str, max_requests: int = 100, window: int = 3600) -> Tuple[bool, float]:
    """
    Check rate limit for an identifier

    Args:
        identifier: Unique identifier for the client
        max_requests: Maximum requests allowed in the window (default 100 per hour)
        window: Time window in seconds (default 1 hour)

    Returns:
        Tuple of (is_allowed, retry_after_seconds)
    """
    # Override with environment variables if available
    max_requests = int(
        __import__('os').environ.get('RATE_LIMIT_MAX', max_requests)
    )
    window = int(
        __import__('os').environ.get('RATE_LIMIT_WINDOW', window)
    )

    return rate_limiter.is_allowed(identifier, max_requests, window)