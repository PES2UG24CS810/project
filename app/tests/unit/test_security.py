"""
Unit tests for security module

US-05: Authentication and authorization testing
"""
import pytest
from fastapi import HTTPException
from app.core.security import verify_api_key, sanitize_text, validate_language_code


@pytest.mark.asyncio
async def test_verify_api_key_valid():
    """Test API key verification with valid key."""
    valid_key = "test-key-123"
    result = await verify_api_key(valid_key)
    assert result == valid_key


@pytest.mark.asyncio
async def test_verify_api_key_invalid():
    """Test API key verification with invalid key."""
    with pytest.raises(HTTPException) as exc_info:
        await verify_api_key("invalid-key")
    assert exc_info.value.status_code == 401
    assert "Invalid API key" in exc_info.value.detail


@pytest.mark.asyncio
async def test_verify_api_key_empty():
    """Test API key verification with empty key."""
    with pytest.raises(HTTPException) as exc_info:
        await verify_api_key("")
    assert exc_info.value.status_code == 401


def test_sanitize_text_normal():
    """Test text sanitization with normal text."""
    text = "  Hello World  "
    result = sanitize_text(text)
    assert result == "Hello World"


def test_sanitize_text_null_bytes():
    """Test text sanitization removes null bytes."""
    text = "Hello\x00World"
    result = sanitize_text(text)
    assert "\x00" not in result
    assert result == "HelloWorld"


def test_sanitize_text_max_length():
    """Test text sanitization enforces max length."""
    text = "a" * 10000
    result = sanitize_text(text)
    assert len(result) <= 5000


def test_sanitize_text_empty():
    """Test text sanitization with empty string."""
    result = sanitize_text("")
    assert result == ""


def test_sanitize_text_none():
    """Test text sanitization with None."""
    result = sanitize_text(None)
    assert result == ""


def test_validate_language_code_valid():
    """Test language code validation with valid codes."""
    assert validate_language_code("en") is True
    assert validate_language_code("es") is True
    assert validate_language_code("fr") is True
    assert validate_language_code("EN") is True  # Case insensitive


def test_validate_language_code_invalid():
    """Test language code validation with invalid codes."""
    assert validate_language_code("xx") is False
    assert validate_language_code("invalid") is False
    assert validate_language_code("") is False
