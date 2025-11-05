"""
API v1 Routes for Language Translation API.

Implements translation, language detection, and history endpoints.
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.config import get_session
from app.core.security import verify_api_key, sanitize_text, validate_language_code
from app.core.rate_limiter import check_rate_limit
from app.models.schemas import (
    TranslateRequest,
    TranslateResponse,
    DetectLanguageRequest,
    DetectLanguageResponse,
    HistoryResponse
)
from app.models.history import TranslationHistory
from app.models.db import save_history, get_history_by_key
from app.services.translator import translator_service

router = APIRouter(prefix="/api/v1", tags=["translation"])


@router.post(
    "/translate",
    response_model=TranslateResponse,
    summary="Translate text",
    description="Translate text from source language to target language. Source language can be auto-detected."
)
async def translate_text(
    request: TranslateRequest,
    api_key: str = Depends(verify_api_key),
    _rate_limit: int = Depends(check_rate_limit),
    session: Session = Depends(get_session)
):
    """
    Translate text endpoint.
    
    US-01: As a user, I want to translate text between languages
    
    Args:
        request: Translation request with text and language codes
        api_key: Validated API key
        _rate_limit: Rate limit check (dependency)
        session: Database session
        
    Returns:
        TranslateResponse: Translation results
        
    Raises:
        HTTPException: If validation fails or translation errors occur
    """
    try:
        # Sanitize input text
        if isinstance(request.text, list):
            sanitized_texts = [sanitize_text(t) for t in request.text]
        else:
            sanitized_texts = sanitize_text(request.text)
        
        # Validate target language
        if not validate_language_code(request.target_lang):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported target language: {request.target_lang}"
            )
        
        # Validate source language if provided
        if request.source_lang and not validate_language_code(request.source_lang):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported source language: {request.source_lang}"
            )
        
        # Perform translation
        result = await translator_service.translate(
            text=sanitized_texts,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        # Save to history (save first text if list)
        first_text = sanitized_texts[0] if isinstance(sanitized_texts, list) else sanitized_texts
        first_translation = result["translated_text"][0] if isinstance(result["translated_text"], list) else result["translated_text"]
        
        history_record = TranslationHistory(
            source_text=first_text,
            translated_text=first_translation,
            source_lang=result["source_lang"],
            target_lang=result["target_lang"],
            user_key=api_key,
            timestamp=datetime.utcnow()
        )
        save_history(session, history_record)
        
        # Return response
        return TranslateResponse(
            original_text=request.text,
            translated_text=result["translated_text"],
            source_lang=result["source_lang"],
            target_lang=result["target_lang"],
            timestamp=datetime.utcnow()
        )
        
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(exc)}"
        ) from exc


@router.post(
    "/detect",
    response_model=DetectLanguageResponse,
    summary="Detect language",
    description="Automatically detect the language of the provided text."
)
async def detect_language(
    request: DetectLanguageRequest,
    api_key: str = Depends(verify_api_key),
    _rate_limit: int = Depends(check_rate_limit)
):
    """
    Language detection endpoint.
    
    US-02: As a user, I want to auto-detect the language of text
    
    Args:
        request: Detection request with text
        api_key: Validated API key
        _rate_limit: Rate limit check (dependency)
        
    Returns:
        DetectLanguageResponse: Detected language and confidence
        
    Raises:
        HTTPException: If detection fails
    """
    try:
        # Sanitize input
        sanitized_text = sanitize_text(request.text)
        
        # Detect language
        detected_lang, confidence = await translator_service.detect_language(sanitized_text)
        
        return DetectLanguageResponse(
            text=request.text,
            detected_lang=detected_lang,
            confidence=round(confidence, 4)
        )
        
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Language detection failed: {str(exc)}"
        ) from exc


@router.get(
    "/history",
    response_model=List[HistoryResponse],
    summary="Get translation history",
    description="Retrieve translation history for the authenticated user."
)
async def get_translation_history(
    limit: int = 100,
    api_key: str = Depends(verify_api_key),
    _rate_limit: int = Depends(check_rate_limit),
    session: Session = Depends(get_session)
):
    """
    Get translation history endpoint.
    
    US-03: As a user, I want to retrieve my translation history
    
    Args:
        limit: Maximum number of records to return (default: 100)
        api_key: Validated API key
        _rate_limit: Rate limit check (dependency)
        session: Database session
        
    Returns:
        List[HistoryResponse]: List of translation history records
    """
    try:
        # Validate limit
        if limit < 1 or limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 1000"
            )
        
        # Retrieve history
        history_records = get_history_by_key(session, api_key, limit)
        
        return [HistoryResponse.from_orm(record) for record in history_records]
        
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve history: {str(exc)}"
        ) from exc
