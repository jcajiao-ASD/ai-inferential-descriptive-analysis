"""
Integration tests for the Healthcheck API endpoints.

This module contains tests that verify the healthcheck endpoint
functionality when integrated with the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestHealthcheckEndpoint:

    """Tests for the healthcheck API endpoint."""

    def test_healthcheck_returns_200(self, client):
        """Test that the healthcheck endpoint returns a 200 OK status code."""
        # Act
        response = client.get("/api/healthcheck")

        # Assert
        assert response.status_code == 200

    def test_healthcheck_returns_ok_status(self, client):
        """Test that the healthcheck endpoint returns the correct status message."""
        # Act
        response = client.get("/api/healthcheck")

        # Assert
        assert response.json() == {"status": "OK"}

    def test_healthcheck_returns_json_content_type(self, client):
        """Test that the healthcheck endpoint returns JSON content."""
        # Act
        response = client.get("/api/healthcheck")

        # Assert
        assert response.headers["Content-Type"] == "application/json"

    def test_healthcheck_rejects_head_request(self, client):
        """Test that the healthcheck endpoint responds to HEAD requests."""
        # Act
        response = client.head("/api/healthcheck")

        # Assert
        assert response.status_code == 405
