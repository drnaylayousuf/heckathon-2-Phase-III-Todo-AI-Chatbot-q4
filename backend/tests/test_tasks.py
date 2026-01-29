"""
Tests for task endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.models.task import TaskStatus, TaskPriority


def test_create_task(client):
    """Test creating a new task."""
    # First register and login to get a token
    client.post(
        "/api/register",
        json={
            "email": "task_test@example.com",
            "password": "password123",
            "name": "Task Test User"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "task_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    # Create a task
    response = client.post(
        "/api/user_id/tasks",  # We need to get the actual user ID
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Since we need the actual user ID, let's get it first
    user_response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    user_id = user_response.json()["id"]

    # Now create the task with the actual user ID
    response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["priority"] == "medium"
    assert data["status"] == "pending"


def test_get_user_tasks(client):
    """Test retrieving user's tasks."""
    # Register and login
    client.post(
        "/api/register",
        json={
            "email": "get_tasks_test@example.com",
            "password": "password123",
            "name": "Get Tasks Test User"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "get_tasks_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]
    user_response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    user_id = user_response.json()["id"]

    # Create a task first
    client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Get Tasks Test",
            "description": "Test for getting tasks",
            "priority": "high"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get tasks
    response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    task_found = False
    for task in data:
        if task["title"] == "Get Tasks Test":
            task_found = True
            break
    assert task_found


def test_update_task(client):
    """Test updating a task."""
    # Register and login
    client.post(
        "/api/register",
        json={
            "email": "update_task_test@example.com",
            "password": "password123",
            "name": "Update Task Test User"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "update_task_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]
    user_response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    user_id = user_response.json()["id"]

    # Create a task first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Original Task",
            "description": "Original description",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    task_id = create_response.json()["id"]

    # Update the task
    update_response = client.put(
        f"/api/{user_id}/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "description": "Updated description",
            "priority": "high"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["description"] == "Updated description"
    assert updated_task["priority"] == "high"


def test_delete_task(client):
    """Test deleting a task."""
    # Register and login
    client.post(
        "/api/register",
        json={
            "email": "delete_task_test@example.com",
            "password": "password123",
            "name": "Delete Task Test User"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "delete_task_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]
    user_response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    user_id = user_response.json()["id"]

    # Create a task first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Task to Delete",
            "description": "This will be deleted",
            "priority": "low"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    task_id = create_response.json()["id"]

    # Delete the task
    delete_response = client.delete(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_response.status_code == 200

    # Verify the task is gone
    get_response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    tasks = get_response.json()
    task_exists = False
    for task in tasks:
        if task["id"] == task_id:
            task_exists = True
            break
    assert not task_exists


def test_complete_task(client):
    """Test marking a task as complete."""
    # Register and login
    client.post(
        "/api/register",
        json={
            "email": "complete_task_test@example.com",
            "password": "password123",
            "name": "Complete Task Test User"
        }
    )

    login_response = client.post(
        "/api/login",
        data={
            "username": "complete_task_test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]
    user_response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    user_id = user_response.json()["id"]

    # Create a task first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Task to Complete",
            "description": "This will be marked as complete",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    task_id = create_response.json()["id"]

    # Mark the task as complete
    complete_response = client.patch(
        f"/api/{user_id}/tasks/{task_id}/complete",
        json={"completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert complete_response.status_code == 200
    completed_task = complete_response.json()
    assert completed_task["status"] == "completed"