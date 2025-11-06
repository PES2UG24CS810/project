"""
Translation Service for Language Translation API.

Provides language detection and mock translation functionality.
"""
from typing import Dict, List, Tuple
import langdetect
from langdetect import detect_langs, LangDetectException
from app.core.config import settings


class TranslatorService:
    """
    Translation service for handling text translation and language detection.
    
    Uses langdetect for language detection and provides deterministic
    mock translation for testing purposes.
    """
    
    def __init__(self):
        """Initialize the translator service."""
        # Set seed for deterministic language detection in tests
        langdetect.DetectorFactory.seed = 0
    
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to detect language from
            
        Returns:
            Tuple[str, float]: (language_code, confidence_score)
            
        Raises:
            ValueError: If language cannot be detected
        """
        if not text or len(text.strip()) < 3:
            raise ValueError("Text too short for language detection")
        
        try:
            langs = detect_langs(text)
            if langs:
                # Return the most probable language
                best = langs[0]
                return best.lang, best.prob
            raise ValueError("Could not detect language")
        except LangDetectException as exc:
            raise ValueError(f"Language detection failed: {str(exc)}") from exc
    
    async def translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> str:
        """
        Translate single text from source to target language.
        
        This is a deterministic mock translation that adds a prefix.
        In production, this would call an actual translation API.
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            str: Translated text
        """
        # Validate languages are supported
        supported = settings.get_supported_languages()
        if target_lang.lower() not in supported:
            raise ValueError(f"Unsupported target language: {target_lang}")
        
        # Mock translation: add prefix with target language
        if source_lang == target_lang:
            return text
        
        # Deterministic mock translation
        translated = f"[Translated to {target_lang}]: {text}"
        return translated
    
    async def translate(
        self,
        text: str | List[str],
        source_lang: str | None,
        target_lang: str
    ) -> Dict:
        """
        Translate text or list of texts.
        
        Args:
            text: Single text or list of texts to translate
            source_lang: Source language (None for auto-detect)
            target_lang: Target language code
            
        Returns:
            dict: Translation results with original, translated, source/target langs
        """
        # Handle single text vs list
        is_list = isinstance(text, list)
        texts = text if is_list else [text]
        
        # Handle empty text
        if not texts or (len(texts) == 1 and not texts[0]):
            return {
                "original_text": text,
                "translated_text": "" if not is_list else [],
                "source_lang": source_lang or "en",
                "target_lang": target_lang
            }
        
        # Auto-detect source language if not provided
        if not source_lang:
            try:
                detected_lang, _ = await self.detect_language(texts[0])
                source_lang = detected_lang
            except ValueError:
                # Default to English if detection fails
                source_lang = "en"
        
        # Translate each text
        translations = []
        for txt in texts:
            if txt:
                translated = await self.translate_text(txt, source_lang, target_lang)
                translations.append(translated)
            else:
                translations.append("")
        
        # Return in the same format as input (single or list)
        result = {
            "original_text": text,
            "translated_text": translations if is_list else translations[0],
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        return result


# Global translator instance
translator_service = TranslatorService()
