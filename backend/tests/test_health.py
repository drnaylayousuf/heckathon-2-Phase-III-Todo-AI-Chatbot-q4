"""
Tests for health check endpoint
"""
import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data == {"status": "healthy"}


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data == {"message": "Welcome to the Hackathon Todo API"}