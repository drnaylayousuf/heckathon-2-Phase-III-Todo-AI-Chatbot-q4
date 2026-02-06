#!/usr/bin/env python3
"""
Test script to verify frontend-backend connection
"""

import requests
import time
import subprocess
import os
from threading import Thread

def test_backend_connection():
    """Test if the backend API is accessible"""
    print("Testing backend connection...")

    # Test both local and Hugging Face URLs
    urls_to_test = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space"
    ]

    for url in urls_to_test:
        try:
            print(f"Testing {url}...")
            response = requests.get(f"{url}/health", timeout=10)
            if response.status_code == 200:
                print(f"[OK] {url} is accessible - Status: {response.json()}")
                return url
            else:
                print(f"[FAIL] {url} returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[FAIL] {url} failed with error: {e}")

    return None

def test_specific_endpoints(base_url):
    """Test specific API endpoints"""
    print(f"\nTesting specific endpoints on {base_url}...")

    endpoints = [
        "/",
        "/health",
        "/api/health",
        "/status/ready",
        "/status/alive"
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            status = "[OK]" if response.status_code == 200 else "[FAIL]"
            print(f"  {status} {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  [FAIL] {endpoint} - Error: {e}")

def start_backend_server():
    """Start the backend server in a separate thread"""
    print("Starting backend server...")
    try:
        # Start the backend server
        process = subprocess.Popen(
            ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Give the server time to start
        time.sleep(5)
        return process
    except Exception as e:
        print(f"Failed to start backend server: {e}")
        return None

def main():
    print("=== Frontend-Backend Connection Test ===\n")

    # First, test if backend is already running
    accessible_url = test_backend_connection()

    if accessible_url:
        print(f"\n✓ Backend is accessible at {accessible_url}")
        test_specific_endpoints(accessible_url)
    else:
        print("\n✗ Backend is not accessible. Attempting to start server...")
        # Try to start the backend server
        server_process = start_backend_server()

        if server_process:
            print("Waiting for server to start...")
            time.sleep(5)

            # Test again
            accessible_url = test_backend_connection()
            if accessible_url:
                print(f"\n✓ Backend is now accessible at {accessible_url}")
                test_specific_endpoints(accessible_url)

                # Keep the server running for manual testing
                print(f"\nServer is running at {accessible_url}")
                print("Press Ctrl+C to stop the server")
                try:
                    server_process.wait()
                except KeyboardInterrupt:
                    print("\nStopping server...")
                    server_process.terminate()
            else:
                print("\n✗ Still unable to connect to backend server")
        else:
            print("✗ Failed to start backend server")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()