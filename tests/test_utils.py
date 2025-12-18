import json
import os
from fastapi.testclient import TestClient
from webapp.run import app
from webapp.mock_objects import MOCK_FRONTEND_PAYLOAD

def update_snapshot_recommendations_response():
    """
    Utility function to update the snapshot_recommendations_response.json file with the current
    response from the /api/recommendations endpoint using MOCK_FRONTEND_PAYLOAD.
    Run manually when you want to refresh the snapshot.
    """
    client = TestClient(app)
    payload = MOCK_FRONTEND_PAYLOAD
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200, f"Request failed: {response.status_code}"
    data = response.json()
    # Write to the snapshot file in the tests directory
    snapshot_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "snapshot_recommendations_response.json")
    print(f"Attempting to write snapshot to: {os.path.abspath(snapshot_path)}")
    try:
        with open(snapshot_path, "w") as f:
            json.dump(data, f, indent=2, sort_keys=False)
        print(f"Snapshot updated successfully: {os.path.abspath(snapshot_path)}")
    except Exception as e:
        print(f"Failed to update snapshot: {e}")
        raise

if __name__ == "__main__":
    update_snapshot_recommendations_response()

