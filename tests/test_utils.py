import json
import os
import pytest
from webapp.models.mock_objects import MOCK_FRONTEND_PAYLOAD
from typing import Any


@pytest.mark.usefixtures("client")
def test_update_snapshot_recommendations_response(client: Any) -> None:
    """
    Update the snapshot_recommendations_response.json file with the current
    response from the /api/recommendations endpoint using MOCK_FRONTEND_PAYLOAD.

    :param client: The FastAPI test client fixture
    :raises AssertionError: If the response status code is not 200
    :raises Exception: If writing the snapshot file fails
    """
    payload = MOCK_FRONTEND_PAYLOAD
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200, f"Request failed: {response.status_code}"
    data = response.json()
    snapshot_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "tests",
        "snapshot_recommendations_response.json",
    )
    print(f"Attempting to write snapshot to: {os.path.abspath(snapshot_path)}")
    try:
        with open(snapshot_path, "w") as f:
            json.dump(data, f, indent=2, sort_keys=False)
        print(f"Snapshot updated successfully: {os.path.abspath(snapshot_path)}")
    except Exception as e:
        print(f"Failed to update snapshot: {e}")
        raise
