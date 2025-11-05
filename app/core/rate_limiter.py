"""
Rate Limiter module for API request throttling.

Simple in-memory rate limiter that tracks requests per API key/IP.
"""
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from app.core.config import settings


class RateLimiter:
    """
    In-memory rate limiter.
    
    Tracks requests per identifier (API key or IP) within a time window.
    """
    
    def __init__(self, max_requests: int = 100, window_minutes: int = 1):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in the window
            window_minutes: Time window in minutes
        """
        self.max_requests = max_requests
        self.window = timedelta(minutes=window_minutes)
        self.requests: Dict[str, list] = defaultdict(list)
    
    def _clean_old_requests(self, identifier: str):
        """
        Remove requests outside the current time window.
        
        Args:
            identifier: API key or IP address
        """
        cutoff = datetime.now() - self.window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]
    
    def check_rate_limit(self, identifier: str) -> Tuple[bool, int]:
        """
        Check if identifier has exceeded rate limit.
        
        Args:
            identifier: API key or IP address
            
        Returns:
            Tuple[bool, int]: (is_allowed, remaining_requests)
        """
        self._clean_old_requests(identifier)
        
        current_requests = len(self.requests[identifier])
        is_allowed = current_requests < self.max_requests
        remaining = max(0, self.max_requests - current_requests)
        
        return is_allowed, remaining
    
    def add_request(self, identifier: str):
        """
        Record a new request for the identifier.
        
        Args:
            identifier: API key or IP address
        """
        self.requests[identifier].append(datetime.now())


# Global rate limiter instance
rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_per_minute,
    window_minutes=1
)


async def check_rate_limit(request: Request, api_key: str):
    """
    Dependency to check rate limit for a request.
    
    Args:
        request: FastAPI request object
        api_key: Validated API key
        
    Raises:
        HTTPException: If rate limit is exceeded
    """
    # Use API key as identifier, fallback to IP
    identifier = api_key if api_key else request.client.host
    
    is_allowed, remaining = rate_limiter.check_rate_limit(identifier)
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {settings.rate_limit_per_minute} requests per minute."
        )
    
    # Record this request
    rate_limiter.add_request(identifier)
    
    return remaining
