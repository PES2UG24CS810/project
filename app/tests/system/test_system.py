"""
System tests for end-to-end scenarios

Placeholder for system tests that will test the entire application flow.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_system_health():
    """Test system health from end-to-end perspective."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# Additional system tests will be added here in future sprints
