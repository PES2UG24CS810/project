"""
Database model for translation history.

SQLModel-based schema for storing translation records.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class TranslationHistory(SQLModel, table=True):
    """
    Translation history record.
    
    Stores each translation request for audit and history retrieval.
    
    Attributes:
        id: Primary key
        source_text: Original text before translation
        translated_text: Translated text
        source_lang: Source language code
        target_lang: Target language code
        timestamp: When the translation was performed
        user_key: API key of the user who requested translation
    """
    
    id: Optional[int] = Field(default=None, primary_key=True)
    source_text: str = Field(max_length=5000)
    translated_text: str = Field(max_length=5000)
    source_lang: str = Field(max_length=10)
    target_lang: str = Field(max_length=10)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_key: str = Field(max_length=100, index=True)
