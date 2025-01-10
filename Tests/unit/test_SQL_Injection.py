import requests
import json

# Base URL of the Backend
BASE_URL = "http://127.0.0.1:10000"  # Update with your Backend URL
DATA_PATH = "../data/sql_injection_requests.json"

# Load JSON requests for tests
with open(DATA_PATH, "r") as f:
    test_requests = json.load(f)


def test_sql_injection():
    errors = []  # List to store errors for later review

    print("Starting SQL Injection tests...")

    # Step 1: Setup
    try:
        print("[Setup] Registering legitimate user...")
        response = requests.post(f"{BASE_URL}/users/register", json=test_requests["setup"]["register"])
        assert response.status_code == 200, f"Setup failed during registration: {response.json()}"
    except Exception as e:
        errors.append(f"Error in legitimate registration: {e}")

    try:
        print("[Setup] Logging in legitimate user...")
        response = requests.post(f"{BASE_URL}/users/login", json=test_requests["setup"]["login"])
        assert response.status_code == 200, f"Setup failed during login: {response.json()}"
        token = response.json().get("token")
        assert token, "Login did not return a token."
    except Exception as e:
        errors.append(f"Error in legitimate login: {e}")
        token = None

    # Step 2: SQL Injection Tests
    endpoints = [
        ("register", "POST", "/users/register", test_requests["attacks"]["register"], None, 400),
        ("login", "POST", "/users/login", test_requests["attacks"]["login"], None, [400, 401]),
        ("password reset", "POST", "/users/password-reset", test_requests["attacks"]["password_reset"], None, 400),
        ("update user", "PUT", f"/users/{test_requests['attacks']['update_user']['user_id']}", test_requests["attacks"]["update_user"], {"Authorization": f"Bearer {token}"}, 400),
    ]

    for name, method, endpoint, payload, headers, expected_status in endpoints:
        try:
            print(f"[Attack] Testing SQL Injection on {name} endpoint...")
            if method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", json=payload, headers=headers)
            elif method == "PUT":
                response = requests.put(f"{BASE_URL}{endpoint}", json=payload, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")

            assert response.status_code in (expected_status if isinstance(expected_status, list) else [expected_status]), \
                f"Expected {expected_status}, but got {response.status_code}: {response.json()}"
        except Exception as e:
            errors.append(f"Error in SQL Injection test on {name}: {e}")

    # Step 3: Summary
    print("\n--- Test Summary ---")
    if errors:
        print("The following errors occurred:")
        for error in errors:
            print(f"- {error}")
    else:
        print("All tests passed successfully!")



if __name__ == "__main__":
    test_sql_injection()
