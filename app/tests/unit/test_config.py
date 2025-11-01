"""
Unit tests for configuration module
"""
import pytest
from app.core.config import Settings


def test_settings_initialization():
    """Test that Settings class initializes correctly."""
    settings = Settings()
    assert settings.environment == "development"
    assert hasattr(settings, "api_key")
    assert hasattr(settings, "database_url")


def test_get_config():
    """Test get_config returns dictionary."""
    settings = Settings()
    config = settings.get_config()
    assert isinstance(config, dict)
    assert "environment" in config
