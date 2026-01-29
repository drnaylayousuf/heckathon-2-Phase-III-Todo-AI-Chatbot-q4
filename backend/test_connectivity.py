#!/usr/bin/env python3
"""
Simple connectivity test to verify the backend API is accessible
"""

import requests

def test_backend_connectivity():
    try:
        print("Testing backend connectivity...")

        # Test basic connectivity
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")

        # Test health endpoint
        response = requests.get("http://127.0.0.1:8000/health")
        print(f"Health endpoint: {response.status_code} - {response.json()}")

        print("✅ Backend API is accessible!")
        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend API at http://127.0.0.1:8000")
        print("Please make sure your backend server is running.")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    test_backend_connectivity()