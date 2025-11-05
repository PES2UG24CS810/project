"""
Unit tests for rate limiter module

US-06: Rate limiting functionality testing
"""
import pytest
import time
from app.core.rate_limiter import RateLimiter


def test_rate_limiter_initialization():
    """Test rate limiter initializes with correct parameters."""
    limiter = RateLimiter(max_requests=10, window_minutes=1)
    assert limiter.max_requests == 10
    assert limiter.window.total_seconds() == 60


def test_rate_limiter_allows_requests_within_limit():
    """Test rate limiter allows requests within limit."""
    limiter = RateLimiter(max_requests=5, window_minutes=1)
    identifier = "test-key"
    
    for i in range(5):
        is_allowed, remaining = limiter.check_rate_limit(identifier)
        assert is_allowed is True
        assert remaining == 5 - i
        limiter.add_request(identifier)


def test_rate_limiter_blocks_requests_exceeding_limit():
    """Test rate limiter blocks requests exceeding limit."""
    limiter = RateLimiter(max_requests=3, window_minutes=1)
    identifier = "test-key"
    
    # Make 3 requests
    for _ in range(3):
        limiter.add_request(identifier)
    
    # 4th request should be blocked
    is_allowed, remaining = limiter.check_rate_limit(identifier)
    assert is_allowed is False
    assert remaining == 0


def test_rate_limiter_different_identifiers():
    """Test rate limiter tracks different identifiers separately."""
    limiter = RateLimiter(max_requests=2, window_minutes=1)
    
    limiter.add_request("key1")
    limiter.add_request("key1")
    limiter.add_request("key2")
    
    is_allowed_1, _ = limiter.check_rate_limit("key1")
    is_allowed_2, remaining_2 = limiter.check_rate_limit("key2")
    
    assert is_allowed_1 is False
    assert is_allowed_2 is True
    assert remaining_2 == 1


def test_rate_limiter_cleans_old_requests():
    """Test rate limiter cleans old requests outside window."""
    limiter = RateLimiter(max_requests=2, window_minutes=1)
    identifier = "test-key"
    
    # Add 2 requests
    limiter.add_request(identifier)
    limiter.add_request(identifier)
    
    # Should be at limit
    is_allowed, _ = limiter.check_rate_limit(identifier)
    assert is_allowed is False
    
    # Manually set old timestamp
    from datetime import datetime, timedelta
    limiter.requests[identifier][0] = datetime.now() - timedelta(minutes=2)
    
    # Should now allow new request
    is_allowed, remaining = limiter.check_rate_limit(identifier)
    assert is_allowed is True
    assert remaining > 0


def test_rate_limiter_remaining_count():
    """Test rate limiter correctly reports remaining requests."""
    limiter = RateLimiter(max_requests=10, window_minutes=1)
    identifier = "test-key"
    
    _, remaining = limiter.check_rate_limit(identifier)
    assert remaining == 10
    
    limiter.add_request(identifier)
    _, remaining = limiter.check_rate_limit(identifier)
    assert remaining == 9
    
    for _ in range(5):
        limiter.add_request(identifier)
    
    _, remaining = limiter.check_rate_limit(identifier)
    assert remaining == 4
