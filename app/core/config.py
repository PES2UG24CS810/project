"""
Configuration Management for Language Translation API

Handles environment variables, database setup, and application settings.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from sqlmodel import SQLModel, create_engine, Session


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        api_key: API key for external translation services
        database_url: Database connection string
        log_encrypt_key: Key for encrypting sensitive log data
        environment: Application environment (development/production)
        rate_limit_per_minute: Maximum requests per minute per API key
        max_text_length: Maximum length of text to translate
    """
    
    # API Configuration
    api_key: Optional[str] = None
    valid_api_keys: str = "test-key-123,demo-key-456,prod-key-789"
    
    # Database Configuration
    database_url: str = "sqlite:///./translation.db"
    
    # Security Configuration
    log_encrypt_key: str = "default-encryption-key-change-in-production"
    
    # Application Configuration
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    
    # Translation Configuration
    max_text_length: int = 5000
    supported_languages: str = "en,es,fr,de,it,pt,ja,zh,ar,ru,hi,ko"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file_path: str = "./logs/translation_api.log"
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        case_sensitive = False
    
    def get_valid_api_keys(self) -> list:
        """
        Get list of valid API keys.
        
        Returns:
            list: List of valid API key strings
        """
        return [key.strip() for key in self.valid_api_keys.split(",")]
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported language codes.
        
        Returns:
            list: List of supported language codes
        """
        return [lang.strip() for lang in self.supported_languages.split(",")]
    
    def get_config(self) -> dict:
        """
        Get configuration as dictionary.
        
        Returns:
            dict: Configuration settings
        """
        return {
            "environment": self.environment,
            "database_url": self.database_url,
            "rate_limit": self.rate_limit_per_minute,
            "max_text_length": self.max_text_length,
            "supported_languages": self.get_supported_languages()
        }


# Global settings instance
settings = Settings()

# Database engine
engine = create_engine(
    settings.database_url,
    echo=settings.environment == "development",
    connect_args={"check_same_thread": False}  # Needed for SQLite
)


def create_db_and_tables():
    """
    Create database tables.
    
    This should be called on application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Get database session.
    
    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
