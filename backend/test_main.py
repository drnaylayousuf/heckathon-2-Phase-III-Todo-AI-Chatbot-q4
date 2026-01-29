import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_auth_routes_exist():
    """Test that auth routes exist."""
    # Test that we get 422 (validation error) or 405 (method not allowed) for auth routes
    # instead of 404 (not found), which would indicate the routes don't exist
    response = client.get("/api/register")
    assert response.status_code != 404

    response = client.get("/api/login")
    assert response.status_code != 404

def test_tasks_routes_exist():
    """Test that tasks routes exist."""
    # Test that we get 422 (validation error) or 405 (method not allowed) for tasks routes
    # instead of 404 (not found), which would indicate the routes don't exist
    response = client.get("/api/123/tasks")
    assert response.status_code != 404

def test_chat_route_exists():
    """Test that chat route exists."""
    # Test that we get 422 (validation error) or 405 (method not allowed) for chat route
    # instead of 404 (not found), which would indicate the route doesn't exist
    response = client.post("/api/123/chat", json={"message": "hello"})
    assert response.status_code != 404