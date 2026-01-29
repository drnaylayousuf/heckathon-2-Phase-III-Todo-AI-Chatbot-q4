import requests
import json

# Test the API endpoints directly
base_url = "http://127.0.0.1:8000"

print("Testing API endpoints...")

# Test registration
print("\n1. Testing registration...")
try:
    registration_data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Test User"
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

    if reg_response.status_code == 200:
        print("✓ Registration successful!")
        user_data = reg_response.json()
        print(f"Created User ID: {user_data.get('id', 'N/A')}")
    else:
        print(f"✗ Registration failed with status {reg_response.status_code}")

except Exception as e:
    print(f"Registration error: {e}")

# Test login if registration was successful
if reg_response.status_code == 200:
    print("\n2. Testing login...")
    try:
        login_data = {
            "username": "testuser@example.com",
            "password": "testpassword123"
        }

        login_response = requests.post(f"{base_url}/api/login",
                                     data=login_data,
                                     headers={"Origin": "http://localhost:3000"})

        print(f"Login Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")

        if login_response.status_code == 200:
            print("✓ Login successful!")
            token_data = login_response.json()
            print(f"Access Token Type: {token_data.get('token_type', 'N/A')}")
        else:
            print(f"✗ Login failed with status {login_response.status_code}")

    except Exception as e:
        print(f"Login error: {e}")

print("\nAPI test completed.")