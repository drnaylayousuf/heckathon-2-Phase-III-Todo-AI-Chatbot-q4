import requests

# Test the preflight OPTIONS request
print("Testing OPTIONS request...")
try:
    response = requests.options("http://127.0.0.1:8000/api/auth/register",
                              headers={
                                  "Access-Control-Request-Method": "POST",
                                  "Access-Control-Request-Headers": "Content-Type",
                                  "Origin": "http://localhost:3000"
                              })
    print(f"OPTIONS Response Status: {response.status_code}")
    print(f"OPTIONS Response Headers: {dict(response.headers)}")
    print(f"OPTIONS Response Body: {response.text}")
except Exception as e:
    print(f"OPTIONS Request failed: {e}")

print("\nTesting actual POST request...")
try:
    # Test the actual registration endpoint
    response = requests.post("http://127.0.0.1:8000/api/auth/register",
                            json={
                                "email": "test@example.com",
                                "password": "testpassword123",
                                "name": "Test User"
                            },
                            headers={
                                "Content-Type": "application/json",
                                "Origin": "http://localhost:3000"
                            })
    print(f"POST Response Status: {response.status_code}")
    print(f"POST Response Headers: {dict(response.headers)}")
    print(f"POST Response Body: {response.text}")
except Exception as e:
    print(f"POST Request failed: {e}")