import requests

# כתובות השרתים
protected_server_url = "http://localhost:10000/users/register"
vulnerable_server_url = "http://localhost:11000/users/register"

# בדיקות
sql_injection_payload = {
    "full_name": "John Doe",
    "username": "admin' OR '1'='1",
    "email": "sql_injection@example.com",
    "phone_number": "1234567890",
    "password": "SQLiPass123!",
    "confirm_password": "SQLiPass123!",
    "accept_terms": True,
    "gender": "Male"
}

xss_payload = {
    "full_name": "<script>alert('XSS');</script>",
    "username": "xss_test",
    "email": "xss@example.com",
    "phone_number": "1234567890",
    "password": "XSSPass123!",
    "confirm_password": "XSSPass123!",
    "accept_terms": True,
    "gender": "<img src='x' onerror='alert(\"XSS\")'>"
}

# פונקציה לבדוק את השרתים עם payload מסוים
def test_servers(payload, test_name):
    print(f"\nRunning {test_name} Test...")
    for server_name, url in [("Protected Server", protected_server_url), ("Vulnerable Server", vulnerable_server_url)]:
        print(f"\nTesting {server_name} with {test_name}...")
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"Success: {response.json()}")
            else:
                print(f"Failed: {response.status_code}, {response.json()}")
        except Exception as e:
            print(f"Error connecting to {server_name}: {e}")

# הפעלת הבדיקות
if __name__ == "__main__":
    test_servers(sql_injection_payload, "SQL Injection")
    test_servers(xss_payload, "XSS")
