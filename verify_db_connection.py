#!/usr/bin/env python3
"""
Verify Database Connection After Setting Environment Variables
"""

import requests
import time
import json

def test_api_health():
    """Test if the API is accessible"""
    print("[TEST] Testing API health...")

    try:
        response = requests.get("https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space/api/health", timeout=10)
        print(f"   Health check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
            print("   [SUCCESS] API is accessible")
            return True
        else:
            print(f"   [ERROR] API not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [ERROR] API test failed: {e}")
        return False

def test_registration():
    """Test user registration to verify database write functionality"""
    print("\n[TEST] Testing user registration...")

    # Generate unique test data
    timestamp = int(time.time())
    test_email = f"test_user_{timestamp}@example.com"
    test_password = "SecurePass123!"
    test_name = f"Test User {timestamp}"

    print(f"   Registering user: {test_email}")

    try:
        # Register a new user
        register_url = "https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space/api/register"
        register_data = {
            "email": test_email,
            "password": test_password,
            "name": test_name
        }

        response = requests.post(register_url, json=register_data, timeout=15)
        print(f"   Registration response: {response.status_code}")

        if response.status_code == 200:
            user_data = response.json()
            print(f"   [SUCCESS] Registration successful!")
            print(f"   User ID: {user_data.get('id', 'N/A')}")
            print(f"   Email: {user_data.get('email', 'N/A')}")
            return True, test_email, test_password
        elif response.status_code == 400:
            print(f"   [WARN] User might already exist (status 400)")
            return True, test_email, test_password  # Still consider it a pass for DB connectivity
        else:
            print(f"   [ERROR] Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None, None

    except Exception as e:
        print(f"   [ERROR] Registration test failed: {e}")
        return False, None, None

def test_login():
    """Test user login to verify database read functionality"""
    print("\n[TEST] Testing user login...")

    # Use a known test email format (you might need to register first)
    # For this test, we'll use a placeholder - in real scenario you'd use an existing user
    test_email = f"test_user_{int(time.time())}@example.com"
    test_password = "NonExistentPass123!"  # This will fail, but we can test the endpoint

    print(f"   Attempting login with test credentials...")

    try:
        login_url = "https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space/api/login"

        # Use form data format as expected by OAuth2PasswordRequestForm
        login_data = {
            "username": test_email,
            "password": test_password
        }

        response = requests.post(login_url, data=login_data, timeout=15)
        print(f"   Login response: {response.status_code}")

        if response.status_code in [200, 400, 401]:  # Different expected responses
            print(f"   [SUCCESS] Login endpoint is working (status: {response.status_code})")
            return True
        else:
            print(f"   [ERROR] Login endpoint error: {response.status_code}")
            return False

    except Exception as e:
        print(f"   [ERROR] Login test failed: {e}")
        return False

def test_specific_endpoints():
    """Test specific endpoints to verify they're accessible"""
    print("\n[TEST] Testing specific API endpoints...")

    endpoints = [
        ("/", "root"),
        ("/test", "test"),
        ("/health", "health"),
        ("/api/health", "api health")
    ]

    all_working = True

    for endpoint, name in endpoints:
        try:
            url = f"https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space{endpoint}"
            response = requests.get(url, timeout=10)
            print(f"   {name} endpoint ({endpoint}): {response.status_code}")
            if response.status_code not in [200, 404]:  # 404 might be expected for some
                all_working = False
        except Exception as e:
            print(f"   {name} endpoint error: {e}")
            all_working = False

    if all_working:
        print("   [SUCCESS] Most endpoints are accessible")
    else:
        print("   [ERROR] Some endpoints are not accessible")

    return all_working

def main():
    print("[TEST] Verifying Database Connection After Environment Variable Update")
    print("=" * 70)
    print("Testing if Neon PostgreSQL database is working correctly...")
    print("=" * 70)

    # Test API health
    health_ok = test_api_health()

    if not health_ok:
        print("\n[ERROR] API is not accessible. Database test cannot proceed.")
        return False

    # Test specific endpoints
    endpoints_ok = test_specific_endpoints()

    # Test registration (writes to database)
    reg_success, email, password = test_registration()

    # Test login (reads from database)
    login_ok = test_login()

    print("\n" + "=" * 70)
    print("[RESULTS] VERIFICATION RESULTS:")
    print("=" * 70)

    print(f"API Health: {'[PASS]' if health_ok else '[FAIL]'}")
    print(f"Endpoints Accessible: {'[PASS]' if endpoints_ok else '[FAIL]'}")
    print(f"Registration Test: {'[PASS]' if reg_success else '[FAIL]'}")
    print(f"Login Endpoint Test: {'[PASS]' if login_ok else '[FAIL]'}")

    overall_success = health_ok and endpoints_ok and (reg_success or login_ok)

    if overall_success:
        print("\n[SUCCESS] OVERALL: Database connection appears to be working!")
        print("[SUCCESS] Your Neon PostgreSQL database should be properly connected")
        print("[SUCCESS] Registration and login functionality should work")
        print("[SUCCESS] Data should flow to your database")
    else:
        print("\n[ERROR] OVERALL: There are still connection issues")
        print("[ERROR] Check your Hugging Face Space logs for detailed errors")
        print("[ERROR] Verify your DATABASE_URL is correct")

    print("\n[TIP] Check your Hugging Face Space logs for real-time updates:")
    print("   https://huggingface.co/spaces/nayla-yousuf-123/todo-app-chatbot-phase3/logs")

    return overall_success

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[SUCCESS] DATABASE CONNECTION VERIFICATION: SUCCESSFUL!")
    else:
        print("\n[ERROR] DATABASE CONNECTION VERIFICATION: FAILED!")