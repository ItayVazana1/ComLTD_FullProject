import requests

BASE_URL = "http://localhost:10000/users"

def register_user(payload):
    """
    Register a user with valid payload.
    """
    response = requests.post(f"{BASE_URL}/register", json=payload)
    if response.status_code == 200:
        print(f"User {payload['username']} registered successfully.")
        return True
    else:
        print(f"Failed to register user {payload['username']}: {response.text}")
        return False

def test_login(username_or_email, password, expected_status, description):
    """
    Test login for a specific user.
    """
    payload = {
        "username_or_email": username_or_email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)
    print(f"{description} -> Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status, f"{description} failed!"
    print(f"{description} passed.")
    return response.json().get("token") if response.status_code == 200 else None

def test_logout(token, expected_status, description):
    """
    Test logout functionality for a user.
    """
    payload = {"token": token}
    response = requests.post(f"{BASE_URL}/logout", json=payload)
    print(f"{description} -> Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status, f"{description} failed!"
    print(f"{description} passed.")

def test_user_block(username_or_email, correct_password, wrong_password, max_attempts=3):
    """
    Test user block functionality after multiple failed login attempts.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            test_login(username_or_email, wrong_password, 401, f"Attempt {attempt}: Incorrect password")
        except AssertionError:
            print(f"Attempt {attempt}: Incorrect password failed as expected.")

    # Test user is blocked after max attempts
    test_login(username_or_email, correct_password, 403, "User blocked after multiple failed login attempts")

if __name__ == "__main__":
    # Step 1: Register all users
    users = [
        {
            "full_name": "John1 Doe",
            "username": "validuser",
            "email": "validuser@example.com",
            "phone_number": "1234567890",
            "password": "Valid$PassRword123",
            "confirm_password": "Valid$PassRword123",
            "accept_terms": True,
            "gender": "Male"
        },
        {
            "full_name": "John2 Doe",
            "username": "wrongpassworduser",
            "email": "wrongpassworduser@example.com",
            "phone_number": "1234567891",
            "password": "Correct$PasswRord123",
            "confirm_password": "Correct$PasswRord123",
            "accept_terms": True,
            "gender": "Male"
        },
        {
            "full_name": "John3 Doe",
            "username": "inactiveuser",
            "email": "inactiveuser@example.com",
            "phone_number": "1234567892",
            "password": "Inactive$PasTTsword123",
            "confirm_password": "Inactive$PasTTsword123",
            "accept_terms": True,
            "gender": "Male"
        },
        {
            "full_name": "John4 Doe",
            "username": "sqlinjectionuser",
            "email": "sqlinjection@example.com",
            "phone_number": "1234567893",
            "password": "SQLi$PasRs123",
            "confirm_password": "SQLi$PasRs123",
            "accept_terms": True,
            "gender": "Male"
        }
    ]

    for user in users:
        if not register_user(user):
            print(f"Skipping tests for {user['username']} due to registration failure.")
            continue

    # Step 2: Test login scenarios
    # Positive test
    token = test_login("validuser", "Valid$PassRword123", 200, "Valid user login")
    test_login("validuser", "Valid$PassRword123", 409, "User already logged in")

    # Test logout
    if token:
        test_logout(token, 200, "Logout for valid user")

    # Negative tests
    test_login("nonexistentuser", "RandomPassword123", 401, "Non-existent user login")
    test_login("wrongpassworduser", "WrongPass@word123", 401, "Incorrect password login")
    test_login("<script>alert('XSS')</script>", "Random!!Password123", 400, "XSS attempt")
    test_login("' OR '1'='1", "SQLi$Password123", 400, "SQL Injection attempt")
    test_login("", "", 401, "Empty fields login")

    # Step 3: Block user after multiple failed attempts
    test_user_block("validuser", "Valid$PassRword123", "WrongPassword123")
