"""
Unit tests for the healthcheck router.

This module contains tests to verify the functionality of the healthcheck endpoint
in the FastAPI application.
"""

from fastapi.testclient import TestClient
from src.presentation.api.healthcheck import healthcheck_controller

client = TestClient(healthcheck_controller.router)


def test_ping():
    """
    Test the healthcheck endpoint.

    This test verifies that the healthcheck endpoint returns a 200 status code
    and the expected JSON response.
    """
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
