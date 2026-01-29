#!/usr/bin/env python3
"""
Test script to verify task API endpoints
"""

import requests
import json
from app.config import settings

def test_task_endpoints():
    print(f"Testing task API endpoints...")
    print(f"Base URL: http://127.0.0.1:8000")

    # First, let's check if the API is running
    try:
        health_response = requests.get("http://127.0.0.1:8000/health")
        print(f"Health check: {health_response.status_code} - {health_response.json()}")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return

    # Test with a fake user ID to see if the route exists
    fake_user_id = "test-user-id"

    # Test GET /api/{user_id}/tasks (without auth token, expect 401)
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/{fake_user_id}/tasks")
        print(f"GET /api/{fake_user_id}/tasks: {response.status_code}")

        if response.status_code == 401:
            print("✅ Route exists (returns 401 as expected without auth)")
        elif response.status_code == 404:
            print("❌ Route does not exist (returns 404)")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")

    except Exception as e:
        print(f"❌ Error testing route: {e}")

    # Test POST /api/{user_id}/tasks (without auth token, expect 401)
    try:
        response = requests.post(
            f"http://127.0.0.1:8000/api/{fake_user_id}/tasks",
            json={"title": "Test task", "description": "Test description", "priority": "medium"}
        )
        print(f"POST /api/{fake_user_id}/tasks: {response.status_code}")

        if response.status_code == 401:
            print("✅ Route exists (returns 401 as expected without auth)")
        elif response.status_code == 404:
            print("❌ Route does not exist (returns 404)")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")

    except Exception as e:
        print(f"❌ Error testing POST route: {e}")

if __name__ == "__main__":
    test_task_endpoints()