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


def test_detect_language():
    """Test language detection with various texts."""
    translator = TranslatorService()
    
    # English text
    lang, confidence = translator.detect_language("Hello, how are you?")
    assert lang == "en"
    assert 0 < confidence <= 1.0
    
    # Spanish text
    lang, confidence = translator.detect_language("Hola, ¿cómo estás?")
    assert lang == "es"
    assert confidence > 0.5
    
    # French text
    lang, confidence = translator.detect_language("Bonjour, comment allez-vous?")
    assert lang == "fr"
    assert confidence > 0.5


def test_detect_language_short_text():
    """Test language detection with short text."""
    translator = TranslatorService()
    lang, confidence = translator.detect_language("Hi")
    assert lang is not None
    assert confidence >= 0


def test_detect_language_empty_text():
    """Test language detection with empty text."""
    translator = TranslatorService()
    with pytest.raises(Exception):
        translator.detect_language("")


def test_translate_text_single():
    """Test translation of single text."""
    translator = TranslatorService()
    result = translator.translate_text("Hello", "en", "es")
    assert result.startswith("[Translated to es]:")
    assert "Hello" in result


def test_translate_text_different_languages():
    """Test translation to different target languages."""
    translator = TranslatorService()
    
    text = "Hello World"
    result_es = translator.translate_text(text, "en", "es")
    result_fr = translator.translate_text(text, "en", "fr")
    
    assert "[Translated to es]:" in result_es
    assert "[Translated to fr]:" in result_fr
    assert result_es != result_fr


def test_translate_single_text_with_source():
    """Test translate method with single text and source language."""
    translator = TranslatorService()
    result = translator.translate("Hello", "es", "en")
    
    assert isinstance(result, str)
    assert result.startswith("[Translated to es]:")


def test_translate_single_text_without_source():
    """Test translate method with auto-detection."""
    translator = TranslatorService()
    result = translator.translate("Hello", "es", None)
    
    assert isinstance(result, str)
    assert result.startswith("[Translated to es]:")


def test_translate_list_with_source():
    """Test translate method with list of texts."""
    translator = TranslatorService()
    texts = ["Hello", "Good morning", "Thank you"]
    results = translator.translate(texts, "es", "en")
    
    assert isinstance(results, list)
    assert len(results) == 3
    for result in results:
        assert result.startswith("[Translated to es]:")


def test_translate_list_without_source():
    """Test translate method with list and auto-detection."""
    translator = TranslatorService()
    texts = ["Hello", "World"]
    results = translator.translate(texts, "fr", None)
    
    assert isinstance(results, list)
    assert len(results) == 2


def test_translate_empty_text():
    """Test translation with empty text."""
    translator = TranslatorService()
    result = translator.translate("", "es", "en")
    assert result == ""


def test_translate_special_characters():
    """Test translation with special characters."""
    translator = TranslatorService()
    text = "Hello! @#$% World?"
    result = translator.translate(text, "es", "en")
    
    assert text in result
    assert result.startswith("[Translated to es]:")
