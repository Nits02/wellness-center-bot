import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_webhook_success():
    """Test the /webhook endpoint with a valid payload."""
    payload = {
        "user_id": "user123",
        "user_message": "I'd like to book a 2-day gym trial."
    }

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Message received successfully."

def test_webhook_invalid_payload():
    """Test the /webhook endpoint with missing fields."""
    # Missing user_message
    payload = {
        "user_id": "user123"
    }

    response = client.post("/webhook", json=payload)

    # Should fail validation (422 Unprocessable Entity)
    assert response.status_code == 422
