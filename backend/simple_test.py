import requests
import json

# Test the API endpoints directly
base_url = "http://127.0.0.1:8000"

print("Testing API endpoints...")

# Test registration
print("\n1. Testing registration...")
try:
    registration_data = {
        "email": "testuser2@example.com",
        "password": "testpassword123",
        "name": "Test User 2"
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "http://localhost:3000"
    }

    reg_response = requests.post(f"{base_url}/api/register",
                               json=registration_data,
                               headers=headers)

    print(f"Registration Status: {reg_response.status_code}")
    print(f"Registration Response: {reg_response.text}")

except Exception as e:
    print(f"Registration error: {e}")