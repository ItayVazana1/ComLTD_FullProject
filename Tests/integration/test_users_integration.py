import pytest
import sys
import os
import json
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../BackendApp")))
from ...Backend.BackendApp.app.main import app


client = TestClient(app)
DATA_PATH = "../data/users_requests.json"

# Load JSON requests for tests
with open(DATA_PATH, "r") as f:
    test_requests = json.load(f)

def test_user_flow():
    """Test full user flow including registration, login, and update."""
    # Step 1: Register
    response = client.post("/users/register", json=test_requests["register"])
    assert response.status_code == 200
    assert response.json().get("status") == "success"

    # Step 2: Login
    response = client.post("/users/login", json=test_requests["login"])
    assert response.status_code == 200
    assert "token" in response.json()
    token = response.json()["token"]

    # Step 3: Update user details
    user_id = test_requests["update_user"]["user_id"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/users/users/{user_id}", json=test_requests["update_user"]["data"], headers=headers)
    assert response.status_code == 200
    assert response.json().get("status") == "success"
