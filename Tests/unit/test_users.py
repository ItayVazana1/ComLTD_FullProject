import requests
import json

# Base URL of the Backend
BASE_URL = "http://127.0.0.1:10000"  # Update with your Backend URL
DATA_PATH = '../data/users_requests.json'

# Load JSON requests for tests
with open(DATA_PATH, "r") as f:
    test_requests = json.load(f)

def test_user_registration():
    """Test user registration endpoint."""
    print("Testing user registration...")
    response = requests.post(f"{BASE_URL}/users/register", json=test_requests["register"])
    assert response.status_code == 200, f"Failed: {response.json()}"
    user_id = response.json().get("id")  # Save the user_id
    print(f"User id from registration test is - {user_id}")
    assert user_id, "User ID not returned in registration response"
    test_requests["update_user"]["user_id"] = user_id  # Save for update test
    print("User registration test passed!")

def test_user_login():
    """Test user login endpoint."""
    print("Testing user login...")
    response = requests.post(f"{BASE_URL}/users/login", json=test_requests["login"])
    assert response.status_code == 200, f"Failed: {response.json()}"
    token = response.json().get("token")
    print(f"Current Session Token for tested user is - {token}")
    assert token, "Token not returned in login response"
    test_requests["token"] = token  # Save the token for logout
    print("User login test passed!")

def test_password_reset_request():
    """Test password reset request endpoint."""
    print("Testing password reset request...")
    response = requests.post(f"{BASE_URL}/users/password-reset", json=test_requests["password_reset"])
    assert response.status_code == 200, f"Failed: {response.json()}"
    assert response.json().get("status") == "success"
    print("Password reset request test passed!")

def test_password_reset():
    """Test password reset endpoint."""
    print("Testing password reset...")
    reset_token = input("Enter the reset token sent to your email: ")
    test_requests["reset_password"]["reset_token"] = reset_token
    response = requests.post(f"{BASE_URL}/users/reset-password", json=test_requests["reset_password"])
    assert response.status_code == 200, f"Failed: {response.json()}"
    assert response.json().get("status") == "success"
    print("Password reset test passed!")

def test_user_update():
    """Test user update endpoint."""
    print("Testing user update...")
    user_id = test_requests["update_user"].get("user_id")
    assert user_id, "User ID is not available for update test"
    headers = {"Authorization": f"Bearer {test_requests.get('token')}"}
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=test_requests["update_user"], headers=headers)
    assert response.status_code == 200, f"Failed: {response.json()}"
    print("User update test passed!")

def test_user_logout():
    """Test user logout endpoint."""
    print("Testing user logout...")
    token = test_requests.get("token")
    assert token, "Token is not available for logout test"
    logout_payload = {"token": token}
    logout_response = requests.post(f"{BASE_URL}/users/logout", json=logout_payload)
    assert logout_response.status_code == 200, f"Failed: {logout_response.json()}"
    assert logout_response.json().get("status") == "success"
    print("User logout test passed!")


if __name__ == "__main__":
    print("Starting tests...")
    test_user_registration()
    test_user_login()
    test_password_reset_request()
    test_password_reset()
    test_user_update()
    test_user_logout()
    print("All tests completed successfully!")
