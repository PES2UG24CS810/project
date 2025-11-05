"""
Security module for authentication and authorization.

Handles API key validation and security dependencies.
"""
from fastapi import Header, HTTPException, status
from app.core.config import settings


async def verify_api_key(x_api_key: str = Header(..., description="API Key for authentication")) -> str:
    """
    Verify API key from header.
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Returns:
        str: Validated API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    valid_keys = settings.get_valid_api_keys()
    
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing"
        )
    
    if x_api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return x_api_key


def sanitize_text(text: str) -> str:
    """
    Sanitize input text to prevent injection attacks.
    
    Args:
        text: Raw input text
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Limit length
    max_length = settings.max_text_length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_language_code(lang_code: str) -> bool:
    """
    Validate if language code is supported.
    
    Args:
        lang_code: Language code to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    supported = settings.get_supported_languages()
    return lang_code.lower() in supported
