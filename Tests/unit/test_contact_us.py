import requests
import json

BASE_URL = "http://127.0.0.1:10000"
DATA_PATH = "../data/contact_us_requests.json"

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

def test_contact_us_valid_request():
    """Test contact us with a valid request."""
    print("Testing contact us with a valid request...")
    request_data = test_requests["contact_us"]["valid_request"]
    request_data["user_id"] = user_id  # Add user_id dynamically
    response = requests.post(f"{BASE_URL}/contact-us-send", json=request_data)
    assert response.status_code == 200, f"Failed: {response.json()}"
    print("Contact us with valid request test passed!")

def test_contact_us_send_copy_request():
    """Test contact us with send_copy=True."""
    print("Testing contact us with send_copy=True...")
    request_data = test_requests["contact_us"]["send_copy_request"]
    request_data["user_id"] = user_id  # Add user_id dynamically
    response = requests.post(f"{BASE_URL}/contact-us-send", json=request_data)
    assert response.status_code == 200, f"Failed: {response.json()}"
    print("Contact us with send_copy request test passed!")

def test_logout_user():
    """Test logging out a user."""
    print("Testing user logout...")
    response = requests.post(f"{BASE_URL}/users/logout", json={"token": token})
    assert response.status_code == 200, f"Failed: {response.json()}"
    print("User logout test passed!")

if __name__ == "__main__":
    print("Starting contact us tests...")
    test_register_user()
    test_login_user()
    test_contact_us_valid_request()
    test_contact_us_send_copy_request()
    test_logout_user()
    print("All contact us tests completed successfully!")
