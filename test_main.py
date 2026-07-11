import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_webhook_success():
    """Test /webhook books an appointment when AI returns a valid booking intent."""
    parsed_response = {
        "intent": "book_appointment",
        "service": "Ozone Therapy",
        "proposed_time": "2026-07-12T09:00:00",
    }

    with patch("main._parse_scheduling_intent", return_value=parsed_response) as mock_parse, \
         patch("main.get_supabase_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.insert.return_value.execute.return_value = MagicMock()

        payload = {
            "user_id": "user123",
            "user_message": "I want to book ozone therapy for tomorrow morning.",
        }
        response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Ozone Therapy" in data["message"]
    assert "2026-07-12T09:00:00" in data["message"]


def test_webhook_ai_parse_failure():
    """Test /webhook returns error when AI fails to parse intent."""
    with patch("main._parse_scheduling_intent", side_effect=ValueError("AI returned garbage")):
        payload = {
            "user_id": "user123",
            "user_message": "asdfghjkl",
        }
        response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "couldn't understand" in data["message"]


def test_webhook_unknown_intent():
    """Test /webhook returns error when AI cannot determine intent."""
    parsed_response = {
        "intent": "unknown",
        "service": "Unknown",
        "proposed_time": None,
    }

    with patch("main._parse_scheduling_intent", return_value=parsed_response):
        payload = {
            "user_id": "user123",
            "user_message": "What's the weather like?",
        }
        response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "wasn't able to determine" in data["message"]

def test_webhook_invalid_payload():
    """Test the /webhook endpoint with missing fields."""
    # Missing user_message
    payload = {
        "user_id": "user123"
    }

    response = client.post("/webhook", json=payload)

    # Should fail validation (422 Unprocessable Entity)
    assert response.status_code == 422


@pytest.mark.parametrize("count,expected_level", [
    (5, "Less Crowded"),
    (14, "Less Crowded"),
    (15, "Moderate"),
    (25, "Moderate"),
    (35, "Moderate"),
    (36, "Highly Crowded"),
    (50, "Highly Crowded"),
])
@patch("main.get_supabase_client")
def test_current_occupancy(mock_get_client, count, expected_level):
    """Test /current-occupancy returns the correct crowding level."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    # Chain: table().select().order().limit().execute()
    mock_execute = MagicMock()
    mock_execute.data = [{"current_count": count}]
    mock_client.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value = mock_execute

    response = client.get("/current-occupancy")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["current_count"] == count
    assert data["occupancy_level"] == expected_level


@patch("main.get_supabase_client")
def test_current_occupancy_no_data(mock_get_client):
    """Test /current-occupancy when no occupancy data exists."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_execute = MagicMock()
    mock_execute.data = []
    mock_client.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value = mock_execute

    response = client.get("/current-occupancy")
    assert response.status_code == 200
    assert response.json()["status"] == "no_data"
