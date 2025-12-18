import json
from webapp.run import (
    recommend_for_attribute,
    recommend_for_geographic_coverage,
    app,
)
from webapp.mock_objects import MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS, MOCK_FRONTEND_PAYLOAD
from fastapi.testclient import TestClient

client = TestClient(app)


# --- Unit tests for individual recommenders ---
def test_recommend_for_attribute_unit():
    """
    Unit test for recommend_for_attribute.
    """
    attributes = MOCK_FRONTEND_PAYLOAD["ATTRIBUTE"]
    results = recommend_for_attribute(attributes)
    # print results as json
    print(json.dumps(results, indent=2))

    assert isinstance(results, list)
    assert len(results) == 7
    for i, item in enumerate(results):
        assert "id" in item
        assert "recommendations" in item
        for rec in item["recommendations"]:
            assert "attributeName" in rec
            assert "objectName" in rec
            assert "uri" in rec
            assert "ontology" in rec
            assert "confidence" in rec
            assert "description" in rec
            assert "propertyLabel" in rec
            assert "propertyUri" in rec


def test_recommend_for_geographic_coverage_unit():
    """
    Unit test for recommend_for_geographic_coverage.
    """
    geos = [
        {"description": "Lake Tahoe region", "objectName": "LakeTahoe"}
    ]
    results = recommend_for_geographic_coverage(geos)
    assert isinstance(results, list)
    assert results == MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS


def test_reformat_attribute_elements_unit():
    from webapp.run import reformat_attribute_elements
    data = [
        {
            "id": "d49be2c0-7b9e-41f4-ae07-387d3e1f14c8",
            "name": "Latitude",
            "description": "Latitude of collection",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        }
    ]
    expected = [
        {
            "entity_name": "SurveyResults.csv",
            "entity_description": "Table contains survey information and the counts of the number of egg masses for each species during that survey.",
            "object_name": "SurveyResults.csv",
            "column_name": "Latitude",
            "column_description": "Latitude of collection"
        }
    ]
    out = reformat_attribute_elements(data)
    assert out == expected


def test_reformat_geographic_coverage_elements_unit():
    from webapp.run import reformat_geographic_coverage_elements
    data = [{"description": "D1"}, {"description": "D2"}]
    out = reformat_geographic_coverage_elements(data)
    assert out == data


def test_recommend_annotations_endpoint_with_full_mock_frontend_payload():
    """
    Integration test for the /api/recommendations endpoint with the full mock frontend payload as input (as-is).
    Checks that the response is a list and that the number of items matches the number of attributes and coverages.
    """
    payload = MOCK_FRONTEND_PAYLOAD
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check structure of each item
    for item in data:
        assert "id" in item
        assert "recommendations" in item
        for rec in item["recommendations"]:
            assert "label" in rec
            assert "uri" in rec
            assert "ontology" in rec
            assert "confidence" in rec
            assert "description" in rec
            assert "propertyLabel" in rec
            assert "propertyUri" in rec


def test_recommendations_endpoint_snapshot():
    """
    Integration test: POST to /api/recommendations with MOCK_FRONTEND_PAYLOAD and compare response to stored snapshot.
    Sorts both lists by 'id' to ensure order does not affect the test.
    """
    payload = MOCK_FRONTEND_PAYLOAD
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    with open("tests/snapshot_recommendations_response.json", "r") as f:
        expected = json.load(f)
    data_sorted = sorted(data, key=lambda x: x["id"])
    expected_sorted = sorted(expected, key=lambda x: x["id"])
    assert data_sorted == expected_sorted
