import pytest
from fastapi.testclient import TestClient
from webapp.run import app
from webapp.models.mock_objects import MOCK_FRONTEND_PAYLOAD, MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def mock_payload():
    return MOCK_FRONTEND_PAYLOAD

@pytest.fixture(scope="session")
def mock_geo_coverage():
    return MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS

