"""
Database Models - Placeholder

This module will contain database models and ORM configurations.
"""
from typing import Optional
from datetime import datetime


class TranslationLog:
    """
    Placeholder model for translation log entries.
    
    This will be implemented with proper ORM (SQLAlchemy) in future sprints.
    """
    
    def __init__(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        translated_text: Optional[str] = None
    ):
        """
        Initialize translation log entry.
        
        Args:
            text: Original text
            source_lang: Source language
            target_lang: Target language
            translated_text: Translated text
        """
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translated_text = translated_text
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """
        Convert to dictionary representation.
        
        Returns:
            dict: Log entry as dictionary
        """
        return {
            "text": self.text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "translated_text": self.translated_text,
            "timestamp": self.timestamp.isoformat()
        }
