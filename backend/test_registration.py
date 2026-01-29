#!/usr/bin/env python3
"""
Test script to manually test the registration process
"""

import requests
import json
from app.config import settings

def test_registration():
    # Clear all users first
    print(f"Database URL: {settings.database_url}")
    print("Testing registration process...")

    # Test with a new user
    test_user = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }

    print(f"Attempting to register: {test_user['email']}")

    try:
        # Make a registration request
        response = requests.post(
            "http://127.0.0.1:8000/api/register",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json=test_user
        )

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        try:
            response_json = response.json()
            print(f"Response Body: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful!")
            print(f"Registered user: {response_json}")
        elif response.status_code == 400:
            print("❌ Registration failed - Bad Request")
        elif response.status_code == 422:
            print("❌ Registration failed - Validation Error")
        else:
            print(f"❌ Registration failed - Status Code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server. Is the backend running on http://127.0.0.1:8000?")
    except Exception as e:
        print(f"❌ Error during registration test: {e}")

if __name__ == "__main__":
    test_registration()