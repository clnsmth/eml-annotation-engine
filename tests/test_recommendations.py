from webapp.run import (
    recommend_for_dataset,
    recommend_for_attribute,
    recommend_for_entity,
    recommend_for_geographic_coverage,
    reformat_dataset_elements,
    reformat_attribute_elements,
    reformat_entity_elements,
    reformat_geographic_coverage_elements,
    app,
)
from fastapi.testclient import TestClient

client = TestClient(app)


# --- Unit tests for individual recommenders ---
def test_recommend_for_dataset_unit():
    """
    Unit test for recommend_for_dataset.
    """
    datasets = [
        {"title": "Example Dataset", "creator": "Jane Doe"},
        {"title": "Another Dataset", "creator": "John Smith"},
    ]
    results = recommend_for_dataset(datasets)
    assert isinstance(results, list)
    assert len(results) == 2
    for i, item in enumerate(results):
        assert item["id"] == f"dataset-{i}"
        assert "recommendations" in item
        rec = item["recommendations"][0]
        assert rec["label"] == "Survey Dataset"
        assert rec["ontology"] == "IAO"


def test_recommend_for_attribute_unit():
    """
    Unit test for recommend_for_attribute.
    """
    attributes = [
        {"name": "SurveyID", "type": "string"},
        {"name": "SampleID", "type": "int"},
    ]
    results = recommend_for_attribute(attributes)
    assert isinstance(results, list)
    assert len(results) == 2
    for i, item in enumerate(results):
        assert item["id"] == f"attribute-{i}"
        assert "recommendations" in item
        rec = item["recommendations"][0]
        assert rec["label"] == "Identifier"
        assert rec["ontology"] == "IAO"


def test_recommend_for_entity_unit():
    """
    Unit test for recommend_for_entity.
    """
    entities = [
        {"name": "Lake", "type": "waterbody"},
        {"name": "River", "type": "waterbody"},
    ]
    results = recommend_for_entity(entities)
    assert isinstance(results, list)
    assert len(results) == 2
    for i, item in enumerate(results):
        assert item["id"] == f"entity-{i}"
        assert "recommendations" in item
        rec = item["recommendations"][0]
        assert rec["label"] == "Lake"
        assert rec["ontology"] == "ENVO"


def test_recommend_for_geographic_coverage_unit():
    """
    Unit test for recommend_for_geographic_coverage.
    """
    geos = [
        {"description": "Lake Tahoe region", "objectName": "LakeTahoe"},
        {"description": "Sierra Nevada", "objectName": "SierraNevada"},
    ]
    results = recommend_for_geographic_coverage(geos)
    assert isinstance(results, list)
    assert len(results) == 2
    for i, item in enumerate(results):
        assert item["id"] == f"geographicCoverage-{i}"
        assert "recommendations" in item
        rec = item["recommendations"][0]
        assert rec["label"] == "Geographic Region"
        assert rec["ontology"] == "ENVO"
        assert rec["attributeName"] == geos[i]["description"]
        assert rec["objectName"] == geos[i]["objectName"]


def test_parse_eml_elements_unit():
    """
    Unit test for parse_eml_elements, now ensures reformatting is applied.
    """
    from webapp.run import parse_eml_elements
    payload = {
        "elements": {
            "dataset": [{"title": "A"}],
            "attribute": [{"name": "B"}],
            "entity": [{"name": "C"}],
            "geographicCoverage": [{"description": "D"}]
        }
    }
    grouped = parse_eml_elements(payload)
    # Each group should be a list containing the reformatted list
    assert set(grouped.keys()) == {"dataset", "attribute", "entity", "geographicCoverage"}
    # Check that the reformatters were applied (for now, just returns input)
    assert grouped["dataset"][0] == reformat_dataset_elements([{"title": "A"}])
    assert grouped["attribute"][0] == reformat_attribute_elements([{"name": "B"}])
    assert grouped["entity"][0] == reformat_entity_elements([{"name": "C"}])
    assert grouped["geographicCoverage"][0] == reformat_geographic_coverage_elements([{"description": "D"}])


def test_reformat_dataset_elements_unit():
    from webapp.run import reformat_dataset_elements
    data = [{"title": "A"}, {"title": "B"}]
    out = reformat_dataset_elements(data)
    assert out == data


def test_reformat_attribute_elements_unit():
    from webapp.run import reformat_attribute_elements
    data = [{"name": "foo"}, {"name": "bar"}]
    out = reformat_attribute_elements(data)
    assert out == data


def test_reformat_entity_elements_unit():
    from webapp.run import reformat_entity_elements
    data = [{"name": "Lake"}, {"name": "River"}]
    out = reformat_entity_elements(data)
    assert out == data


def test_reformat_geographic_coverage_elements_unit():
    from webapp.run import reformat_geographic_coverage_elements
    data = [{"description": "D1"}, {"description": "D2"}]
    out = reformat_geographic_coverage_elements(data)
    assert out == data


# --- Integration tests for the endpoint (keep only those that test the endpoint as a whole) ---
def test_recommendations_endpoint():
    # Minimal example EML metadata payload using a supported type key
    payload = {"elements": {"dataset": [
        {"title": "Example Dataset", "creator": "Jane Doe"}
    ]}}
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


# def test_recommendations_mixed_types():
#     """
#     Test /api/recommendations with multiple types (dataset, attribute, entity).
#     """
#     payload = {"elements": {
#         "dataset": [{"title": "Example Dataset"}],
#         "attribute": [{"name": "SurveyID"}],
#         "entity": [{"name": "Lake"}]
#     }}
#     response = client.post("/api/recommendations", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     ids = [item["id"] for item in data]
#     assert any(i.startswith("dataset-") for i in ids)
#     assert any(i.startswith("attribute-") for i in ids)
#     assert any(i.startswith("entity-") for i in ids)


# --- Example mock POST JSON payload from frontend (to be filled in by user) ---
MOCK_FRONTEND_PAYLOAD = {
    # TODO: Fill in with actual example payload from frontend
    # 'elements': { ... }
}

def test_formatters_with_mock_frontend_payload():
    """
    Test the formatter functions using the example mock POST JSON payload from the frontend.
    This is a placeholder; user should fill in MOCK_FRONTEND_PAYLOAD with real data.
    """
    if not MOCK_FRONTEND_PAYLOAD:
        # Skip test if no payload is provided
        import pytest
        pytest.skip("No mock frontend payload provided.")
    grouped = parse_eml_elements(MOCK_FRONTEND_PAYLOAD)
    # For each group, call the corresponding formatter and check output type
    for group, items in grouped.items():
        if group == "dataset":
            assert isinstance(reformat_dataset_elements(items[0]), list)
        elif group == "attribute":
            assert isinstance(reformat_attribute_elements(items[0]), list)
        elif group == "entity":
            assert isinstance(reformat_entity_elements(items[0]), list)
        elif group == "geographicCoverage":
            assert isinstance(reformat_geographic_coverage_elements(items[0]), list)
