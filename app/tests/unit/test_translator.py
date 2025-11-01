"""
Unit tests for translator service
"""
import pytest
from app.services.translator import TranslatorService


@pytest.mark.asyncio
async def test_translator_initialization():
    """Test translator service initializes correctly."""
    service = TranslatorService(api_key="test_key")
    assert service.api_key == "test_key"


@pytest.mark.asyncio
async def test_translate_placeholder():
    """Test translate method returns expected structure."""
    service = TranslatorService()
    result = await service.translate(
        text="Hello",
        source_lang="en",
        target_lang="es"
    )
    assert "translated_text" in result
    assert "source_language" in result
    assert "target_language" in result
