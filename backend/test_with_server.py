import subprocess
import time
import requests
import json

print("Starting server and testing connection...")

# Start the server in a subprocess
server_process = subprocess.Popen(["uvicorn", "app.main:app", "--reload"],
                                 cwd=".",
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)

# Give the server time to start
time.sleep(5)

print("Server should be running now. Testing API...")

# Test the API endpoints directly
base_url = "http://127.0.0.1:8000"

try:
    # Test registration
    print("\n1. Testing registration...")
    registration_data = {
        "email": "testuser_new@example.com",
        "password": "testpassword123",
        "name": "Test User New"
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

        # Test login with the new user
        print("\n2. Testing login...")
        login_data = {
            "username": "testuser_new@example.com",
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
    else:
        print(f"✗ Registration failed with status {reg_response.status_code}")

except Exception as e:
    print(f"Error during testing: {e}")

# Attempt to terminate the server process
try:
    server_process.terminate()
    server_process.wait(timeout=5)
    print("\nServer terminated successfully.")
except:
    try:
        server_process.kill()
        print("\nServer killed forcefully.")
    except:
        print("\nCould not terminate server process.")