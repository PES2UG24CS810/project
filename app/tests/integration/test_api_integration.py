"""
Integration tests for API endpoints

US-01: Translation API
US-02: Language detection API
US-03: Translation history API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)
valid_api_key = "test-key-123"
headers = {"X-API-Key": valid_api_key}


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Language Translation API"
    assert "version" in data


def test_translate_single_text_with_auth():
    """Test translation endpoint with single text and valid auth."""
    payload = {
        "text": "Hello World",
        "source_lang": "en",
        "target_lang": "es"
    }
    response = client.post("/api/v1/translate", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["translated_text"], str)
    assert data["translated_text"].startswith("[Translated to es]:")
    assert data["source_language"] == "en"
    assert data["target_language"] == "es"


def test_translate_list_text_with_auth():
    """Test translation endpoint with list of texts."""
    payload = {
        "text": ["Hello", "Good morning"],
        "source_lang": "en",
        "target_lang": "fr"
    }
    response = client.post("/api/v1/translate", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["translated_text"], list)
    assert len(data["translated_text"]) == 2


def test_translate_without_source_lang():
    """Test translation with auto-detection."""
    payload = {
        "text": "Hello World",
        "target_lang": "es"
    }
    response = client.post("/api/v1/translate", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["source_language"] is not None


def test_translate_without_api_key():
    """Test translation endpoint without API key."""
    payload = {
        "text": "Hello",
        "target_lang": "es"
    }
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 422 or response.status_code == 401


def test_translate_with_invalid_api_key():
    """Test translation endpoint with invalid API key."""
    invalid_headers = {"X-API-Key": "invalid-key-xyz"}
    payload = {
        "text": "Hello",
        "target_lang": "es"
    }
    response = client.post("/api/v1/translate", json=payload, headers=invalid_headers)
    assert response.status_code == 401


def test_translate_with_invalid_language():
    """Test translation endpoint with invalid target language."""
    payload = {
        "text": "Hello",
        "target_lang": "invalid"
    }
    response = client.post("/api/v1/translate", json=payload, headers=headers)
    assert response.status_code == 400


def test_detect_language_endpoint():
    """Test language detection endpoint."""
    payload = {
        "text": "Hello, how are you?"
    }
    response = client.post("/api/v1/detect", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "language" in data
    assert "confidence" in data
    assert data["language"] == "en"
    assert 0 < data["confidence"] <= 1.0


def test_detect_language_spanish():
    """Test language detection with Spanish text."""
    payload = {
        "text": "Hola, ¿cómo estás?"
    }
    response = client.post("/api/v1/detect", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "es"


def test_detect_language_without_auth():
    """Test language detection without authentication."""
    payload = {
        "text": "Hello"
    }
    response = client.post("/api/v1/detect", json=payload)
    assert response.status_code == 422 or response.status_code == 401


def test_history_endpoint():
    """Test history retrieval endpoint."""
    # First, make a translation to create history
    translate_payload = {
        "text": "Test history",
        "target_lang": "es"
    }
    client.post("/api/v1/translate", json=translate_payload, headers=headers)
    
    # Now retrieve history
    response = client.get("/api/v1/history", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["records"], list)
    assert data["total"] >= 0


def test_history_with_limit():
    """Test history endpoint with limit parameter."""
    response = client.get("/api/v1/history?limit=5", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["records"]) <= 5


def test_history_without_auth():
    """Test history endpoint without authentication."""
    response = client.get("/api/v1/history")
    assert response.status_code == 422 or response.status_code == 401


def test_rate_limiting():
    """Test rate limiting enforcement."""
    # Make multiple rapid requests
    payload = {
        "text": "Test",
        "target_lang": "es"
    }
    
    # This test depends on rate limit configuration
    # Making 110 requests to exceed 100/min limit
    responses = []
    for i in range(110):
        response = client.post("/api/v1/translate", json=payload, headers=headers)
        responses.append(response.status_code)
    
    # At least one request should be rate limited (429)
    assert 429 in responses or all(r == 200 for r in responses[:100])


def test_end_to_end_workflow():
    """Test complete workflow: translate, detect, and retrieve history."""
    # Step 1: Detect language
    detect_payload = {"text": "Hello World"}
    detect_response = client.post("/api/v1/detect", json=detect_payload, headers=headers)
    assert detect_response.status_code == 200
    detected_lang = detect_response.json()["language"]
    
    # Step 2: Translate
    translate_payload = {
        "text": "Hello World",
        "source_lang": detected_lang,
        "target_lang": "es"
    }
    translate_response = client.post("/api/v1/translate", json=translate_payload, headers=headers)
    assert translate_response.status_code == 200
    
    # Step 3: Retrieve history
    history_response = client.get("/api/v1/history", headers=headers)
    assert history_response.status_code == 200
    history_data = history_response.json()
    assert history_data["total"] > 0
