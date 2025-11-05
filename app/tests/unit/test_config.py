"""
Unit tests for configuration module

US-04: Configuration management testing
"""
import pytest
from app.core.config import Settings, settings, create_db_and_tables


def test_settings_initialization():
    """Test that Settings class initializes correctly."""
    test_settings = Settings()
    assert test_settings.environment == "development"
    assert hasattr(test_settings, "api_key")
    assert hasattr(test_settings, "database_url")
    assert hasattr(test_settings, "valid_api_keys")


def test_get_config():
    """Test get_config returns dictionary with expected keys."""
    config = settings.get_config()
    assert isinstance(config, dict)
    assert "environment" in config
    assert "database_url" in config
    assert "rate_limit" in config
    assert "max_text_length" in config
    assert "supported_languages" in config


def test_get_valid_api_keys():
    """Test retrieval of valid API keys list."""
    keys = settings.get_valid_api_keys()
    assert isinstance(keys, list)
    assert len(keys) > 0
    assert "test-key-123" in keys


def test_get_supported_languages():
    """Test retrieval of supported languages list."""
    langs = settings.get_supported_languages()
    assert isinstance(langs, list)
    assert len(langs) > 0
    assert "en" in langs
    assert "es" in langs


def test_default_values():
    """Test default configuration values."""
    test_settings = Settings()
    assert test_settings.rate_limit_per_minute == 100
    assert test_settings.max_text_length == 5000
    assert test_settings.port == 8000
    assert test_settings.host == "0.0.0.0"


def test_database_url():
    """Test database URL configuration."""
    assert settings.database_url is not None
    assert "sqlite" in settings.database_url.lower()


def test_create_db_and_tables():
    """Test database table creation."""
    # Should not raise any exceptions
    create_db_and_tables()
