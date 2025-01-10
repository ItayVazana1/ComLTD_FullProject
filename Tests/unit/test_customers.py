import requests
import json

BASE_URL = "http://127.0.0.1:10000"
DATA_PATH = "../data/customers_requests.json"

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

def test_create_multiple_customers():
    """Test creating multiple customers."""
    print("Testing creation of multiple customers...")
    for customer_request in test_requests["customers"]:
        customer_request["user_id"] = user_id  # Add user_id dynamically
        response = requests.post(f"{BASE_URL}/customers/", json=customer_request)
        assert response.status_code == 200, f"Failed: {response.json()}"
        customer_id = response.json().get("id")
        assert customer_id, "Customer ID not returned in creation response"
        customer_request["id"] = customer_id  # Save for further tests
        print(f"Created customer: {customer_request['first_name']} {customer_request['last_name']} with ID: {customer_id}")

    print("Multiple customer creation test passed!")

def test_get_all_customers():
    """Test fetching all customers."""
    print("Testing fetching all customers...")
    response = requests.get(f"{BASE_URL}/customers/", json={"user_id": user_id})
    assert response.status_code == 200, f"Failed: {response.json()}"
    customers = response.json()
    assert isinstance(customers, list), "Response is not a list"
    assert len(customers) >= len(test_requests["customers"]), "Not all customers were returned"

    # הדפסת כל הלקוחות
    print("\nFetched Customers:")
    for customer in customers:
        print(f"ID: {customer['id']}, Name: {customer['first_name']} {customer['last_name']}")

    print("Fetch all customers test passed!")

def test_get_customer():
    """Test fetching a specific customer."""
    print("Testing fetching a customer...")
    for customer_request in test_requests["customers"]:
        customer_id = customer_request.get("id")
        assert customer_id, "Customer ID is not available for fetching test"
        response = requests.get(f"{BASE_URL}/customers/{customer_id}", json={"user_id": user_id})
        assert response.status_code == 200, f"Failed: {response.json()}"
        print(f"Fetched customer with ID: {customer_id}")

    print("Fetch specific customer test passed!")

def test_update_customer():
    """Test updating a customer."""
    print("Testing updating a customer...")
    customer_id = test_requests["customers"][0].get("id")  # Update the first customer
    assert customer_id, "Customer ID is not available for update test"
    customer_update_request = {
        "user_id": user_id,
        "first_name": "Updated First Name",
        "last_name": "Updated Last Name",
        "phone_number": "5550000000",
        "email_address": "updatedemail@example.com",
        "address": "Updated Address",
        "package_id": "pak-3",
        "gender": "Other"
    }
    response = requests.put(f"{BASE_URL}/customers/update_customer/{customer_id}", json=customer_update_request)
    assert response.status_code == 200, f"Failed: {response.json()}"
    print(f"Customer with ID: {customer_id} updated successfully.")

    print("Customer update test passed!")

def test_delete_customer():
    """Test deleting a customer."""
    print("Testing deleting a customer...")
    customer_id = test_requests["customers"][-1].get("id")  # Delete the last customer
    assert customer_id, "Customer ID is not available for delete test"
    response = requests.delete(f"{BASE_URL}/customers/delete_customer/{customer_id}", json={"user_id": user_id})
    assert response.status_code == 200, f"Failed: {response.json()}"
    print(f"Customer with ID: {customer_id} deleted successfully.")

    print("Customer deletion test passed!")

def test_logout_user():
    """Test logging out a user."""
    print("Testing user logout...")
    response = requests.post(f"{BASE_URL}/users/logout", json={"token": token})
    assert response.status_code == 200, f"Failed: {response.json()}"
    print("User logout test passed!")

if __name__ == "__main__":
    print("Starting customers tests...")
    test_register_user()
    test_login_user()
    test_create_multiple_customers()
    test_get_all_customers()
    test_get_customer()
    test_update_customer()
    test_delete_customer()
    test_logout_user()
    print("All customer tests completed successfully!")
