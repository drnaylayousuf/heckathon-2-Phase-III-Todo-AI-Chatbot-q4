"""
Tests for chat endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_chat_endpoint(client):
    """Test the chat endpoint."""
    # Register and login to get a token
    client.post(
        "/api/register",
        json={
            "email": "chat_test@example.com",
            "password": "password123",
            "name": "Chat Test User"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "chat_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]
    user_response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    user_id = user_response.json()["id"]

    # Test the chat endpoint with a simple message
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "message": "Hello, how are you?"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "conversation_id" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0


def test_chat_add_task(client):
    """Test using chat to add a task."""
    # Register and login to get a token
    client.post(
        "/api/register",
        json={
            "email": "chat_add_task_test@example.com",
            "password": "password123",
            "name": "Chat Add Task Test User"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "chat_add_task_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]
    user_response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    user_id = user_response.json()["id"]

    # Test adding a task via chat
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "message": "Add a task to buy groceries"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "conversation_id" in data
    assert "buy groceries" in data["response"].lower() or "added" in data["response"].lower()


def test_chat_list_tasks(client):
    """Test using chat to list tasks."""
    # Register and login to get a token
    client.post(
        "/api/register",
        json={
            "email": "chat_list_task_test@example.com",
            "password": "password123",
            "name": "Chat List Task Test User"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "chat_list_task_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]
    user_response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    user_id = user_response.json()["id"]

    # First add a task
    client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Test Task for Chat",
            "description": "Created for chat test",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Test listing tasks via chat
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "message": "What tasks do I have?"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "conversation_id" in data
    assert isinstance(data["response"], str)