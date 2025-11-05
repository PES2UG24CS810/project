"""
Database operations for Language Translation API.

Functions for saving and retrieving translation history.
"""
from typing import List
from sqlmodel import Session, select
from app.models.history import TranslationHistory


def save_history(session: Session, record: TranslationHistory) -> TranslationHistory:
    """
    Save translation history record to database.
    
    Args:
        session: Database session
        record: TranslationHistory record to save
        
    Returns:
        TranslationHistory: Saved record with ID
    """
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def get_history_by_key(session: Session, user_key: str, limit: int = 100) -> List[TranslationHistory]:
    """
    Retrieve translation history for a specific API key.
    
    Args:
        session: Database session
        user_key: API key to filter by
        limit: Maximum number of records to return
        
    Returns:
        List[TranslationHistory]: List of history records
    """
    statement = (
        select(TranslationHistory)
        .where(TranslationHistory.user_key == user_key)
        .order_by(TranslationHistory.timestamp.desc())
        .limit(limit)
    )
    results = session.exec(statement)
    return list(results)
