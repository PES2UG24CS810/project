"""
System tests for end-to-end scenarios

US-04: Performance and load testing
US-05: End-to-end workflow testing
"""
import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
valid_api_key = "test-key-123"
headers = {"X-API-Key": valid_api_key}


def test_system_health():
    """Test system health from end-to-end perspective."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_complete_translation_workflow():
    """Test complete workflow from detection to translation to history."""
    # Step 1: Detect language of English text
    detect_payload = {"text": "Good morning, how are you today?"}
    detect_response = client.post("/api/v1/detect", json=detect_payload, headers=headers)
    assert detect_response.status_code == 200
    detected_lang = detect_response.json()["language"]
    assert detected_lang == "en"
    
    # Step 2: Translate using detected language
    translate_payload = {
        "text": "Good morning",
        "source_lang": detected_lang,
        "target_lang": "es"
    }
    translate_response = client.post("/api/v1/translate", json=translate_payload, headers=headers)
    assert translate_response.status_code == 200
    translation = translate_response.json()["translated_text"]
    assert "[Translated to es]:" in translation
    
    # Step 3: Verify history contains the translation
    history_response = client.get("/api/v1/history?limit=10", headers=headers)
    assert history_response.status_code == 200
    history_data = history_response.json()
    assert history_data["total"] > 0


def test_multi_language_translation_workflow():
    """Test translation workflow with multiple languages."""
    languages = ["es", "fr", "de", "it"]
    source_text = "Hello World"
    
    for target_lang in languages:
        payload = {
            "text": source_text,
            "source_lang": "en",
            "target_lang": target_lang
        }
        response = client.post("/api/v1/translate", json=payload, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert f"[Translated to {target_lang}]:" in data["translated_text"]


def test_batch_translation_workflow():
    """Test batch translation of multiple texts."""
    texts = [
        "Hello",
        "Good morning",
        "Thank you",
        "Goodbye"
    ]
    
    payload = {
        "text": texts,
        "source_lang": "en",
        "target_lang": "es"
    }
    
    response = client.post("/api/v1/translate", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["translated_text"], list)
    assert len(data["translated_text"]) == len(texts)


def test_performance_response_time():
    """Test that 95% of requests complete within 2 seconds."""
    num_requests = 20
    response_times = []
    
    payload = {
        "text": "Performance test",
        "target_lang": "es"
    }
    
    for _ in range(num_requests):
        start_time = time.time()
        response = client.post("/api/v1/translate", json=payload, headers=headers)
        end_time = time.time()
        
        assert response.status_code == 200
        response_times.append(end_time - start_time)
    
    # Sort and check 95th percentile
    response_times.sort()
    percentile_95_index = int(0.95 * len(response_times))
    percentile_95_time = response_times[percentile_95_index]
    
    assert percentile_95_time < 2.0, f"95th percentile response time {percentile_95_time}s exceeds 2s"


def test_concurrent_user_simulation():
    """Test system behavior with multiple concurrent requests."""
    num_concurrent = 10
    payload = {
        "text": "Concurrent test",
        "target_lang": "fr"
    }
    
    # Simulate concurrent requests
    for _ in range(num_concurrent):
        response = client.post("/api/v1/translate", json=payload, headers=headers)
        assert response.status_code in [200, 429]  # Either success or rate limited


def test_error_recovery_workflow():
    """Test system recovery from error conditions."""
    # Test with invalid language
    invalid_payload = {
        "text": "Test",
        "target_lang": "invalid"
    }
    response = client.post("/api/v1/translate", json=invalid_payload, headers=headers)
    assert response.status_code == 400
    
    # Test system still works after error
    valid_payload = {
        "text": "Test",
        "target_lang": "es"
    }
    response = client.post("/api/v1/translate", json=valid_payload, headers=headers)
    assert response.status_code == 200


def test_data_persistence_workflow():
    """Test that translation history is properly persisted."""
    # Make unique translation
    unique_text = f"Persistence test {time.time()}"
    payload = {
        "text": unique_text,
        "source_lang": "en",
        "target_lang": "es"
    }
    
    translate_response = client.post("/api/v1/translate", json=payload, headers=headers)
    assert translate_response.status_code == 200
    
    # Retrieve history and verify our translation is there
    history_response = client.get("/api/v1/history?limit=100", headers=headers)
    assert history_response.status_code == 200
    
    records = history_response.json()["records"]
    found = any(unique_text in record["source_text"] for record in records)
    assert found, "Translation not found in history"


def test_authentication_workflow():
    """Test authentication flow with valid and invalid credentials."""
    payload = {"text": "Auth test", "target_lang": "es"}
    
    # Test with valid key
    response = client.post("/api/v1/translate", json=payload, headers=headers)
    assert response.status_code == 200
    
    # Test with invalid key
    invalid_headers = {"X-API-Key": "wrong-key"}
    response = client.post("/api/v1/translate", json=payload, headers=invalid_headers)
    assert response.status_code == 401
    
    # Test without key
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code in [401, 422]


def test_api_endpoint_availability():
    """Test that all required endpoints are available."""
    # Root endpoint
    assert client.get("/").status_code == 200
    
    # Health endpoint
    assert client.get("/health").status_code == 200
    
    # Translation endpoint (with auth)
    payload = {"text": "Test", "target_lang": "es"}
    assert client.post("/api/v1/translate", json=payload, headers=headers).status_code == 200
    
    # Detection endpoint (with auth)
    payload = {"text": "Test"}
    assert client.post("/api/v1/detect", json=payload, headers=headers).status_code == 200
    
    # History endpoint (with auth)
    assert client.get("/api/v1/history", headers=headers).status_code == 200
