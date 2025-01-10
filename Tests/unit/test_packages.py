import requests
import json

BASE_URL = "http://127.0.0.1:10000"
DATA_PATH = "../data/packages_requests.json"

# Load test data
with open(DATA_PATH, "r") as f:
    test_requests = json.load(f)

user_id = None
token = None

def test_register_user():
    """Test registering a new user."""
    print("Testing user registration...")
    response = requests.post(f"{BASE_URL}/users/register", json=test_requests["register_user"])
    assert response.status_code == 200, f"Failed: {response.json()}"
    global user_id
    user_id = response.json().get("id")
    assert user_id, "User ID not returned in registration response"
    print("User registration test passed!")

def test_login_user():
    """Test logging in a user."""
    print("Testing user login...")
    response = requests.post(f"{BASE_URL}/users/login", json=test_requests["login_user"])
    assert response.status_code == 200, f"Failed: {response.json()}"
    global token
    token = response.json().get("token")
    assert token, "Token not returned in login response"
    print("User login test passed!")

def test_create_package():
    """Test creating a new package."""
    print("Testing package creation...")
    package_request = test_requests["create_package"]
    package_request["user_id"] = user_id  # Add user_id dynamically

    # Print request for debugging purposes
    print(f"Request payload: {package_request}")

    response = requests.post(f"{BASE_URL}/packages/new_package", json=package_request)
    assert response.status_code == 200, f"Failed: {response.json()}"
    package_id = response.json().get("id")
    assert package_id, "Package ID not returned in creation response"
    test_requests["create_package"]["id"] = package_id  # Save for further tests
    print("Package creation test passed!")



def test_get_all_packages():
    """Test fetching all packages."""
    print("Testing fetching all packages...")
    response = requests.get(f"{BASE_URL}/packages/", json={"user_id": user_id})
    assert response.status_code == 200, f"Failed: {response.text}"
    packages = response.json()
    assert isinstance(packages, list), "Response is not a list"
    assert len(packages) > 0, "No packages were returned"
    print(f"Fetched {len(packages)} packages for user {user_id}.")
    print("Fetch all packages test passed!")


def test_update_package():
    """Test updating a package."""
    print("Testing updating a package...")
    package_id = test_requests["create_package"]["id"]
    assert package_id, "Package ID is not available for update test"

    package_update_request = test_requests["update_package"]
    package_update_request["user_id"] = user_id  # Add user_id dynamically

    response = requests.put(f"{BASE_URL}/packages/update_package/{package_id}", json=package_update_request)
    assert response.status_code == 200, f"Failed: {response.json()}"
    print("Package update test passed!")


def test_get_package():
    """Test fetching a specific package."""
    print("Testing fetching a package...")
    package_id = test_requests["create_package"].get("id")
    assert package_id, "Package ID not available for fetching test"

    response = requests.get(f"{BASE_URL}/packages/{package_id}")
    assert response.status_code == 200, f"Failed: {response.json()}"

    package = response.json()
    assert package["id"] == package_id, "Fetched package ID does not match"
    print("Package fetch test passed!")


def test_delete_package():
    """Test deleting a package."""
    print("Testing deleting a package...")
    package_id = test_requests["create_package"].get("id")
    assert package_id, "Package ID is not available for delete test"
    delete_request = test_requests["delete_package"]
    delete_request["user_id"] = user_id  # Add user_id dynamically
    response = requests.delete(f"{BASE_URL}/packages/delete_package/{package_id}", json=delete_request)
    assert response.status_code == 200, f"Failed: {response.json()}"
    print("Package deletion test passed!")

def test_logout_user():
    """Test logging out a user."""
    print("Testing user logout...")
    response = requests.post(f"{BASE_URL}/users/logout", json={"token": token})
    assert response.status_code == 200, f"Failed: {response.json()}"
    print("User logout test passed!")


if __name__ == "__main__":
    print("Starting tests...")
    test_register_user()
    test_login_user()
    test_create_package()
    test_get_all_packages()
    test_update_package()
    test_get_all_packages()
    test_get_package()
    test_delete_package()
    test_get_all_packages()
    test_logout_user()
    print("All tests completed successfully!")