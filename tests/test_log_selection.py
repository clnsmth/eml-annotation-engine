"""
Tests for the /api/log-selection endpoint using MOCK_SELECTION.
"""

import pytest
from fastapi.testclient import TestClient
from webapp.run import app
from webapp.models.mock_objects import MOCK_SELECTION


@pytest.fixture(scope="module")
def client():
    """
    Fixture for FastAPI test client using the application instance.
    """
    return TestClient(app)


def test_log_selection_endpoint(client):
    """
    Test that the /api/log-selection endpoint receives and responds correctly to a valid selection log payload.
    """
    response = client.post("/api/log-selection", json=MOCK_SELECTION)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"
