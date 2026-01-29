"""
Tests for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.models.user import User
from app.core.auth import verify_password


def test_register_new_user(client):
    """Test registering a new user."""
    response = client.post(
        "/api/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }
    )
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data
    assert "password_hash" not in data  # Should not expose password hash


def test_login_valid_user(client):
    """Test logging in with valid credentials."""
    # First register a user
    client.post(
        "/api/register",
        json={
            "email": "login_test@example.com",
            "password": "password123",
            "name": "Login Test User"
        }
    )

    # Then try to login
    response = client.post(
        "/api/login",
        data={
            "username": "login_test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/login",
        data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_get_current_user(client):
    """Test getting current user info with valid token."""
    # Register and login to get a token
    client.post(
        "/api/register",
        json={
            "email": "current_user_test@example.com",
            "password": "password123",
            "name": "Current User Test"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "current_user_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    # Get current user info
    response = client.get(
        "/api/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current_user_test@example.com"
    assert data["name"] == "Current User Test"


def test_register_duplicate_email(client):
    """Test registering with duplicate email."""
    # Register first user
    client.post(
        "/api/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "name": "First User"
        }
    )

    # Try to register with same email
    response = client.post(
        "/api/register",
        json={
            "email": "duplicate@example.com",
            "password": "anotherpassword",
            "name": "Second User"
        }
    )

    assert response.status_code == 400