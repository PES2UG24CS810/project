"""
Translation Service for Language Translation API.

Provides language detection and real translation functionality using Google Translate.
"""
from typing import Dict, List, Tuple
import asyncio
from functools import partial
import langdetect
from langdetect import detect_langs, LangDetectException
from googletrans import Translator
from app.core.config import settings


class TranslatorService:
    """
    Translation service for handling text translation and language detection.
    
    Uses langdetect for language detection and Google Translate for real translations.
    """
    
    def __init__(self):
        """Initialize the translator service."""
        # Set seed for deterministic language detection in tests
        langdetect.DetectorFactory.seed = 0
        # Initialize Google Translator
        self.translator = Translator()
    
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
        Translate single text from source to target language using Google Translate.
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            str: Translated text
            
        Raises:
            ValueError: If translation fails or language is unsupported
        """
        # Validate languages are supported
        supported = settings.get_supported_languages()
        if target_lang.lower() not in supported:
            raise ValueError(f"Unsupported target language: {target_lang}")
        
        # If source and target are the same, return original text
        if source_lang == target_lang:
            return text
        
        try:
            # Run translation in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            translate_func = partial(
                self.translator.translate,
                text,
                src=source_lang,
                dest=target_lang
            )
            # Add timeout to prevent hanging
            result = await asyncio.wait_for(
                loop.run_in_executor(None, translate_func),
                timeout=10.0  # 10 second timeout
            )
            return result.text
        except asyncio.TimeoutError as exc:
            raise ValueError("Translation request timed out") from exc
        except Exception as exc:
            # If Google Translate fails, provide helpful error
            raise ValueError(f"Translation failed: {str(exc)}") from exc
    
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
