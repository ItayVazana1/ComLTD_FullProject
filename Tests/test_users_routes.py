import json
import requests
from loguru import logger

logger.add("Tests_Logs/test_users_routes.log", rotation="1 MB")
TEST_CASES_FILE = "JSON_files_test/users_req.json"


# טעינת מקרי מבחן מקובץ JSON
def load_test_cases(file_path):
    try:
        with open(file_path, "r") as file:
            test_cases = json.load(file).get("test_cases", [])
            logger.info(f"Successfully loaded {len(test_cases)} test cases.")
            return test_cases
    except Exception as e:
        logger.error(f"Failed to load test cases: {e}")
        return []

# Execute a single test case
def execute_test_case(test_case, user_ids):
    try:
        # Handle dependency if exists
        dependency = test_case.get("dependency")
        if dependency and dependency in user_ids:
            user_id = user_ids[dependency]
        else:
            user_id = ""

        # Replace placeholders in the URL
        url = test_case["url"].replace("{user_id}", user_id)
        method = test_case["method"]
        data = test_case.get("data", {})

        # Execute the HTTP request
        logger.info(f"Executing test case: {test_case['name']} ({method} {url})")
        response = requests.request(method, url, json=data)

        # Log the response
        logger.info(f"Response ({response.status_code}): {response.json()}")

        # Store user_id from response if applicable
        if "Register" in test_case["name"] or "Login" in test_case["name"]:
            user_ids[test_case["name"]] = response.json().get("id")

        # Verify status code
        if response.status_code != test_case["expected_status"]:
            logger.error(f"Test case failed: {test_case['name']} - Expected {test_case['expected_status']}, got {response.status_code}")
        else:
            logger.info(f"Test case passed: {test_case['name']}")

    except Exception as e:
        logger.error(f"Error executing test case {test_case['name']}: {e}")

# פונקציה ראשית
def main():
    file_path = TEST_CASES_FILE
    test_cases = load_test_cases(file_path)
    user_ids = {}  # To store user IDs dynamically

    for test_case in test_cases:
        execute_test_case(test_case, user_ids)  # Pass user_ids as an argument


if __name__ == "__main__":
    main()