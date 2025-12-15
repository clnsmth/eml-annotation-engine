import pytest
from fastapi.testclient import TestClient
from webapp.run import app

client = TestClient(app)


def test_recommendations_endpoint():
    # Minimal example EML metadata payload
    payload = {"elements": {"title": "Example Dataset", "creator": "Jane Doe"}}
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check that each item has 'id' and 'recommendations' keys
    for item in data:
        assert "id" in item
        assert "recommendations" in item
        assert isinstance(item["recommendations"], list)
        # Check that each recommendation has required keys
        for rec in item["recommendations"]:
            assert "label" in rec
            assert "uri" in rec
            assert "ontology" in rec
            assert "confidence" in rec
            assert "description" in rec
            assert "propertyLabel" in rec
            assert "propertyUri" in rec
            # Optional keys: attributeName, objectName (may not be present in all)
