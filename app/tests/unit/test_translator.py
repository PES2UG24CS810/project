"""
Unit tests for translator service

US-01: Translation functionality
US-02: Language detection functionality
"""
import pytest
from app.services.translator import TranslatorService


def test_translator_initialization():
    """Test translator service initializes correctly."""
    translator = TranslatorService()
    assert translator is not None


@pytest.mark.asyncio
async def test_detect_language():
    """Test language detection with various texts."""
    translator = TranslatorService()
    
    # English text
    lang, confidence = await translator.detect_language("Hello, how are you?")
    assert lang == "en"
    assert 0 < confidence <= 1.0
    
    # Spanish text
    lang, confidence = await translator.detect_language("Hola, ¿cómo estás?")
    assert lang == "es"
    assert confidence > 0.5
    
    # French text
    lang, confidence = await translator.detect_language("Bonjour, comment allez-vous?")
    assert lang == "fr"
    assert confidence > 0.5


@pytest.mark.asyncio
async def test_detect_language_short_text():
    """Test language detection with short text."""
    translator = TranslatorService()
    with pytest.raises(ValueError):
        await translator.detect_language("Hi")


@pytest.mark.asyncio
async def test_detect_language_empty_text():
    """Test language detection with empty text."""
    translator = TranslatorService()
    with pytest.raises(ValueError):
        await translator.detect_language("")


@pytest.mark.asyncio
async def test_translate_text_single():
    """Test translation of single text."""
    translator = TranslatorService()
    result = await translator.translate_text("Hello", "en", "es")
    assert result.startswith("[Translated to es]:")
    assert "Hello" in result


@pytest.mark.asyncio
async def test_translate_text_different_languages():
    """Test translation to different target languages."""
    translator = TranslatorService()
    
    text = "Hello World"
    result_es = await translator.translate_text(text, "en", "es")
    result_fr = await translator.translate_text(text, "en", "fr")
    
    assert "[Translated to es]:" in result_es
    assert "[Translated to fr]:" in result_fr
    assert result_es != result_fr


@pytest.mark.asyncio
async def test_translate_single_text_with_source():
    """Test translate method with single text and source language."""
    translator = TranslatorService()
    result = await translator.translate("Hello", "en", "es")
    
    assert isinstance(result, dict)
    assert "translated_text" in result
    assert result["translated_text"].startswith("[Translated to es]:")


@pytest.mark.asyncio
async def test_translate_single_text_without_source():
    """Test translate method with auto-detection."""
    translator = TranslatorService()
    result = await translator.translate("Hello", None, "es")
    
    assert isinstance(result, dict)
    assert "translated_text" in result
    assert result["translated_text"].startswith("[Translated to es]:")


@pytest.mark.asyncio
async def test_translate_list_with_source():
    """Test translate method with list of texts."""
    translator = TranslatorService()
    texts = ["Hello", "Good morning", "Thank you"]
    result = await translator.translate(texts, "en", "es")
    
    assert isinstance(result, dict)
    assert isinstance(result["translated_text"], list)
    assert len(result["translated_text"]) == 3
    for trans in result["translated_text"]:
        assert trans.startswith("[Translated to es]:")


@pytest.mark.asyncio
async def test_translate_list_without_source():
    """Test translate method with list and auto-detection."""
    translator = TranslatorService()
    texts = ["Hello", "World"]
    result = await translator.translate(texts, None, "fr")
    
    assert isinstance(result, dict)
    assert isinstance(result["translated_text"], list)
    assert len(result["translated_text"]) == 2


@pytest.mark.asyncio
async def test_translate_empty_text():
    """Test translation with empty text."""
    translator = TranslatorService()
    result = await translator.translate("", "en", "es")
    assert result["translated_text"] == ""


@pytest.mark.asyncio
async def test_translate_special_characters():
    """Test translation with special characters."""
    translator = TranslatorService()
    text = "Hello! @#$% World?"
    result = await translator.translate(text, "en", "es")
    
    assert text in result["translated_text"]
    assert result["translated_text"].startswith("[Translated to es]:")
