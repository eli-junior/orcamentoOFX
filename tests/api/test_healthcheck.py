import pytest
from ninja.testing import TestClient
from backend.api.healthcheck import router
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    return TestClient(router)


def test_health_success(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == "UP!"


def test_ready_success(client):
    with patch("django.db.connection.cursor", return_value=MagicMock()) as mock_cursor:
        mock_cursor.return_value.__enter__.return_value.execute.return_value = None
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"database": "Ready"}


def test_ready_failure(client):
    # Simulate a database failure by patching the connection cursor
    with patch("django.db.connection.cursor", return_value=MagicMock()) as mock_cursor:
        mock_cursor.side_effect = Exception("Database error")
        response = client.get("/ready")
        assert response.status_code == 503
        assert response.json() == {"detail": "{'database': 'Database error'}"}
