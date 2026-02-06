#!/usr/bin/env python3
"""
API and Database Connectivity Tester
"""

import os
import sys
import requests
import json
import time
import uuid
from datetime import datetime

def test_api_endpoints():
    """Test the API endpoints"""
    print("🔍 Testing API endpoints...")

    # Use the deployed URL
    base_url = "https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space"

    # Test health endpoint
    try:
        print("   Testing /api/health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"   Health check: {response.status_code} - {response.text}")

        if response.status_code == 200:
            print("   ✅ API is accessible")
        else:
            print("   ❌ API is not accessible")
            return False
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        return False

    # Test test endpoint
    try:
        print("   Testing /test endpoint...")
        response = requests.get(f"{base_url}/test", timeout=10)
        print(f"   Test endpoint: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Test endpoint failed: {e}")

    return True

def test_registration_login():
    """Test registration and login functionality"""
    print("\n🔍 Testing registration and login...")

    base_url = "https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space"

    # Generate unique test email
    test_email = f"test_{int(time.time())}@example.com"
    test_password = "TestPassword123!"
    test_name = "Test User"

    print(f"   Using test email: {test_email}")

    # Test registration
    try:
        print("   Attempting registration...")
        reg_payload = {
            "email": test_email,
            "password": test_password,
            "name": test_name
        }

        response = requests.post(
            f"{base_url}/api/register",
            json=reg_payload,
            timeout=15
        )

        print(f"   Registration response: {response.status_code}")
        print(f"   Registration body: {response.text}")

        if response.status_code == 200:
            print("   ✅ Registration successful")
        elif response.status_code == 400:
            print("   ⚠️  Registration failed (possibly email already exists)")
        else:
            print(f"   ❌ Registration failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Registration test failed: {e}")
        return False

    # Test login
    try:
        print("   Attempting login...")
        login_data = {
            "username": test_email,
            "password": test_password
        }

        response = requests.post(
            f"{base_url}/api/login",
            data=login_data,  # Use form data for OAuth2PasswordRequestForm
            timeout=15
        )

        print(f"   Login response: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Login successful")
            # Try to get the token if successful
            try:
                data = response.json()
                if 'access_token' in data:
                    print("   ✅ Got access token")
                    return True
                else:
                    print("   ⚠️  No token in response")
            except:
                print("   ⚠️  Could not parse response JSON")
        else:
            print(f"   ❌ Login failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Login test failed: {e}")
        return False

    return True

def main():
    print("🚀 Starting API and Database Connectivity Test")
    print("=" * 60)

    # Test API endpoints
    api_ok = test_api_endpoints()

    if not api_ok:
        print("\n❌ API is not accessible. Cannot test database functionality.")
        return False

    # Test registration/login functionality
    auth_ok = test_registration_login()

    print("\n" + "=" * 60)
    if api_ok and auth_ok:
        print("✅ All tests passed!")
        print("✅ API is accessible and functional")
        print("✅ Registration and login work correctly")
        print("✅ Data should be flowing to Neon PostgreSQL")
    else:
        print("❌ Some tests failed")
        print("   Check your Hugging Face Space logs for errors")

    print("\n💡 To see real-time logs, check your Hugging Face Space logs:")
    print("   https://huggingface.co/spaces/nayla-yousuf-123/todo-app-chatbot-phase3/logs")

    return api_ok and auth_ok

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n⚠️  Check your environment variables and database connection!")
        sys.exit(1)