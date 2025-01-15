import requests

BASE_URL = "http://localhost:10000/users"

def register_user(full_name, username, email, phone_number, password, gender, expected_status, description):
    payload = {
        "full_name": full_name,
        "username": username,
        "email": email,
        "phone_number": phone_number,
        "password": password,
        "confirm_password": password,
        "accept_terms": True,
        "gender": gender
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)
    print(f"{description} -> Request: {payload}, Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status, f"{description} failed! Response: {response.json()}"
    print(f"{description} passed.")


def test_password_reset_request(email, expected_status, description):
    payload = {"email": email}
    response = requests.post(f"{BASE_URL}/ask-for-password-reset", json=payload)
    print(f"{description} -> Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status, f"{description} failed!"
    print(f"{description} passed.")
    return response.json().get("reset_token") if response.status_code == 200 else None

def test_reset_password(reset_token, new_password, confirm_password, expected_status, description):
    payload = {
        "reset_token": reset_token,
        "new_password": new_password,
        "confirm_password": confirm_password
    }
    response = requests.post(f"{BASE_URL}/reset-password", json=payload)
    print(f"{description} -> Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status, f"{description} failed!"
    print(f"{description} passed.")

def test_change_password(username, current_password, new_password, confirm_password, expected_status, description):
    payload = {
        "username": username,
        "current_password": current_password,
        "new_password": new_password,
        "confirm_password": confirm_password
    }
    response = requests.post(f"{BASE_URL}/change-password-authenticated", json=payload)
    print(f"{description} -> Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status, f"{description} failed!"
    print(f"{description} passed.")


def test_confirm_reset_password(reset_token, new_password, confirm_password, expected_status, description):
    """
    Test the password reset confirmation functionality.
    """
    payload = {
        "reset_token": reset_token,
        "new_password": new_password,
        "confirm_password": confirm_password
    }
    response = requests.post(f"{BASE_URL}/confirm-reset-password", json=payload)
    print(f"{description} -> Request: {payload}, Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status, f"{description} failed! Response: {response.json()}"
    print(f"{description} passed.")

def test_logout(user_id, token, expected_status, description):
    """
    Test the logout functionality.

    :param user_id: ID of the user attempting to logout.
    :param token: Authentication token of the user.
    :param expected_status: Expected HTTP status code.
    :param description: Description of the test case.
    """
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"user_id": user_id, "token": token}  # Include the token in the payload

    # Log request details
    print(f"Logout Request -> Headers: {headers}, Payload: {payload}")

    # Send the logout request
    response = requests.post(f"{BASE_URL}/logout", json=payload, headers=headers)
    print(f"{description} -> Status: {response.status_code}, Response: {response.json()}")

    # Validate response
    assert response.status_code == expected_status, f"{description} failed!"
    print(f"{description} passed.")


def test_full_password_management_flow():
    full_name = "Itay Vaz"
    username = "ItayVaz87"
    email = "vazanaitay3133@gmail.com"
    phone_number = "0509653133"
    password = "Valid%Pa$$word123"
    gender = "Male"

    # Register user
    register_user(full_name, username, email, phone_number, password, gender, 200, "Register a new user")

    # Request password reset
    reset_token = test_password_reset_request(email, 200, "Password reset request with valid email")
    assert reset_token, "Reset token was not generated"

    # Confirm reset password
    new_password = "CELL#vaz!#847"
    test_confirm_reset_password(reset_token, new_password, new_password, 200, "Confirm reset password with valid token and password")

    # Login after password reset
    login_payload = {"username_or_email": username, "password": new_password}
    login_response = requests.post(f"{BASE_URL}/login", json=login_payload)
    print(f"Login after password reset -> Status: {login_response.status_code}, Response: {login_response.json()}")
    assert login_response.status_code == 200, "Login after password reset failed!"

    # Change password
    new_password_2 = "Another$Pa##word456"
    test_change_password(username, new_password, new_password_2, new_password_2, 200, "Change password with valid credentials")

    # Logout after changing the password
    user_id = login_response.json().get("id")
    token = login_response.json().get("token")
    assert user_id, "User ID not found in login response"
    assert token, "Token not found in login response"
    test_logout(user_id, token, 200, "Logout after password change")

    # Login after password change
    login_payload = {"username_or_email": username, "password": new_password_2}
    login_response = requests.post(f"{BASE_URL}/login", json=login_payload)
    print(f"Login after password change -> Status: {login_response.status_code}, Response: {login_response.json()}")
    assert login_response.status_code == 200, "Login after password change failed!"
    user_id = login_response.json().get("id")
    token = login_response.json().get("token")

    # Logout after password change
    test_logout(user_id, token, 200, "Logout after password change")


if __name__ == "__main__":
    test_full_password_management_flow()


