"""
Request and response schemas for API endpoints.

Pydantic models for input validation and output serialization.
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class TranslateRequest(BaseModel):
    """
    Request model for translation endpoint.
    
    Attributes:
        text: Single text or list of texts to translate
        source_lang: Source language code (optional, can be auto-detected)
        target_lang: Target language code
    """
    
    text: str | List[str] = Field(..., description="Text or list of texts to translate")
    source_lang: Optional[str] = Field(None, description="Source language code (auto-detect if not provided)")
    target_lang: str = Field(..., description="Target language code")
    
    @validator('target_lang')
    def validate_target_lang(cls, v):
        """Validate target language is not empty"""
        if not v or not v.strip():
            raise ValueError("Target language is required")
        return v.lower().strip()
    
    @validator('source_lang')
    def validate_source_lang(cls, v):
        """Normalize source language"""
        if v:
            return v.lower().strip()
        return v


class TranslateResponse(BaseModel):
    """
    Response model for translation endpoint.
    
    Attributes:
        original_text: Original input text
        translated_text: Translated text
        source_lang: Detected or provided source language
        target_lang: Target language
        timestamp: When translation was performed
    """
    
    original_text: str | List[str]
    translated_text: str | List[str]
    source_lang: str
    target_lang: str
    timestamp: datetime


class DetectLanguageRequest(BaseModel):
    """
    Request model for language detection endpoint.
    
    Attributes:
        text: Text to detect language from
    """
    
    text: str = Field(..., min_length=1, max_length=5000)


class DetectLanguageResponse(BaseModel):
    """
    Response model for language detection endpoint.
    
    Attributes:
        text: Input text
        detected_lang: Detected language code
        confidence: Confidence score (0-1)
    """
    
    text: str
    detected_lang: str
    confidence: float


class HistoryResponse(BaseModel):
    """
    Response model for history endpoint.
    
    Attributes:
        id: Record ID
        source_text: Original text
        translated_text: Translated text
        source_lang: Source language
        target_lang: Target language
        timestamp: When translation occurred
    """
    
    id: int
    source_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    timestamp: datetime
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True


class ErrorResponse(BaseModel):
    """
    Error response model.
    
    Attributes:
        detail: Error message
        code: Error code (optional)
    """
    
    detail: str
    code: Optional[str] = None
