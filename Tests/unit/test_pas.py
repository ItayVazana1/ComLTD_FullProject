import requests
import random
import string
from colorama import Fore, Style


BASE_URL = "http://localhost:10000/users"

# Test password validation scenarios based on .env rules
PASSWORD_TESTS = [
    {"password": "password", "valid": False, "reason": "Blocked word"},  # Blocked word
    {"password": "admin", "valid": False, "reason": "Blocked word"},  # Blocked word
    {"password": "123", "valid": False, "reason": "Too short"},   # Too short
    {"password": "short1!", "valid": False, "reason": "Missing upper character"},  # Missing upper character
    {"password": "NoSpecialCharacter1", "valid": False, "reason": "Missing special character"},  # Missing special character
    {"password": "NoNumber!", "valid": False, "reason": "Missing number"},  # Missing number
    {"password": "ABCSEF87!", "valid": False, "reason": "Missing lower character"},  # Missing lower character
    {"password": "ValidMongoBongo123!", "valid": True, "reason": "Valid password"},  # Valid password
    {"password": "AnotherValid123!", "valid": True, "reason": "Valid password"},  # Valid password
]


def generate_unique_user_data(base_password):
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return {
        "full_name": f"Test User {random_suffix}",
        "username": f"testuser_{random_suffix}",
        "email": f"testuser_{random_suffix}@example.com",
        "phone_number": "1234567890",
        "password": base_password,
        "confirm_password": base_password,
        "accept_terms": True,
        "gender": "Male"
    }


def test_register():
    for test in PASSWORD_TESTS:
        user_data = generate_unique_user_data(test["password"])
        response = requests.post(
            f"{BASE_URL}/register",
            json=user_data,
        )
        if test["valid"]:
            assert response.status_code == 200, f"Registration with password {test['password']} should have passed"
            print(
                f"Registration with password {Fore.GREEN}{test['password']}{Style.RESET_ALL} passed as expected , reason -> {Fore.GREEN}{test['reason']}{Style.RESET_ALL}")
        else:
            assert response.status_code == 400, f"Registration with password {test['password']} should have failed"
            print(
                f"Registration with password {Fore.RED}{test['password']}{Style.RESET_ALL} failed as expected , reason -> {Fore.RED}{test['reason']}{Style.RESET_ALL}")


if __name__ == "__main__":
    # Run all tests
    test_register()
