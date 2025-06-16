"""
Integration tests for the Pokemon Controller API endpoints.

This module contains tests that verify the behavior of the Pokemon API endpoints
when integrated with the FastAPI application, testing the flow from HTTP request
to response including dependencies, error handling and HTTP headers.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from src.domain.entities.pokemon import Pokemon
from src.domain.exceptions.pokemon import PokemonNotFoundError
from src.infrastructure.service.pokeapi_client import PokeApiHttpClient
from src.presentation.api.v1.dependencies import get_pokemon_api_client


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """
    Fixture to provide the FastAPI application instance for testing.

    Returns
    -------
    FastAPI
        The FastAPI application instance.

    """
    from main import app as fastapi_app

    return fastapi_app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    """
    Fixture to provide a TestClient instance for testing the FastAPI application.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Returns
    -------
    TestClient
        The TestClient instance for making HTTP requests to the application.

    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_pokemon_api_client(client: TestClient):
    """
    Fixture to provide a mock implementation of the Pokemon API client.

    Parameters
    ----------
    client : TestClient
        The TestClient instance for making HTTP requests to the application.

    Yields
    ------
    AsyncMock
        A mock instance of the PokeApiHttpClient.

    """
    mock_client_instance = AsyncMock(spec_async=PokeApiHttpClient)

    def override_get_pokemon_api_client_provider():
        return mock_client_instance

    client.app.dependency_overrides[get_pokemon_api_client] = (
        override_get_pokemon_api_client_provider
    )

    yield mock_client_instance

    del client.app.dependency_overrides[get_pokemon_api_client]


@pytest.fixture
def override_pokemon_api_client_dependency(
    client: TestClient, mock_pokemon_api_client_instance: AsyncMock
):
    """
    Override the Pokemon API client dependency with a mock instance for testing.

    Parameters
    ----------
    client : TestClient
        The TestClient instance for making HTTP requests to the application.
    mock_pokemon_api_client_instance : AsyncMock
        A mock instance of the PokeApiHttpClient.

    Yields
    ------
    AsyncMock
        The mock instance of the PokeApiHttpClient.

    """

    def override_get_pokemon_api_client():
        return mock_pokemon_api_client_instance

    client.app.dependency_overrides[get_pokemon_api_client] = override_get_pokemon_api_client

    yield mock_pokemon_api_client_instance

    del client.app.dependency_overrides[get_pokemon_api_client]


class TestPokemonController:
    """
    Test suite for the Pokemon Controller API endpoints.

    This class contains test cases to verify the behavior of the Pokemon API endpoints,
    including successful responses, error handling, and validation of HTTP status codes
    and response payloads.
    """

    def test_get_pokemon_by_id_success(
        self, client: TestClient, mock_pokemon_api_client: AsyncMock
    ):
        """
        Test the successful retrieval of a Pokemon by its ID.

        Parameters
        ----------
        client : TestClient
            The TestClient instance for making HTTP requests to the application.
        mock_pokemon_api_client : AsyncMock
            A mock instance of the PokeApiHttpClient.

        Verifies
        --------
        - The response status code is 200 OK.
        - The response payload matches the expected Pokemon data.
        - The Cache-Control header is set correctly.
        - The mock API client is called with the correct Pokemon ID.

        """
        pokemon_id = 25
        expected_pokemon = Pokemon(id=pokemon_id, name="pikachu", types=["electric"])

        mock_pokemon_api_client.get_pokemon_by_id.return_value = expected_pokemon

        response = client.get(f"/api/v1/pokemon/{pokemon_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": pokemon_id, "name": "pikachu", "types": ["electric"]}
        assert "Cache-Control" in response.headers
        assert response.headers["Cache-Control"] == "public, max-age=3600"

        mock_pokemon_api_client.get_pokemon_by_id.assert_called_once_with(pokemon_id)

    def test_get_pokemon_by_id_not_found(
        self, client: TestClient, mock_pokemon_api_client: AsyncMock
    ):
        """
        Test the behavior when a Pokemon with the given ID is not found.

        Parameters
        ----------
        client : TestClient
            The TestClient instance for making HTTP requests to the application.
        mock_pokemon_api_client : AsyncMock
            A mock instance of the PokeApiHttpClient.

        Verifies
        --------
        - The response status code is 404 NOT FOUND.
        - The response payload contains the appropriate error message.
        - The mock API client is called with the correct Pokemon ID.

        """
        pokemon_id = 9999

        mock_pokemon_api_client.get_pokemon_by_id.side_effect = PokemonNotFoundError(pokemon_id)

        response = client.get(f"/api/v1/pokemon/{pokemon_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": f"Pokemon with ID {pokemon_id} not found."}

        mock_pokemon_api_client.get_pokemon_by_id.assert_called_once_with(pokemon_id)

    def test_get_pokemon_by_id_internal_error(
        self, client: TestClient, mock_pokemon_api_client: AsyncMock
    ):
        """
        Test the behavior when an internal server error occurs while retrieving a Pokemon by its ID.

        Parameters
        ----------
        client : TestClient
            The TestClient instance for making HTTP requests to the application.
        mock_pokemon_api_client : AsyncMock
            A mock instance of the PokeApiHttpClient.

        Verifies
        --------
        - The response status code is 500 INTERNAL SERVER ERROR.
        - The response payload contains the appropriate error message.
        - The mock API client is called with the correct Pokemon ID.

        """
        pokemon_id = 25

        mock_pokemon_api_client.get_pokemon_by_id.side_effect = Exception(
            "Simulated internal error"
        )

        response = client.get(f"/api/v1/pokemon/{pokemon_id}")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"detail": "An internal server error occurred."}

        mock_pokemon_api_client.get_pokemon_by_id.assert_called_once_with(pokemon_id)

    def test_get_pokemon_by_id_invalid_id(self, client: TestClient):
        """
        Test the behavior when an invalid Pokemon ID is provided.

        Parameters
        ----------
        client : TestClient
            The TestClient instance for making HTTP requests to the application.

        Verifies
        --------
        - The response status code is 422 UNPROCESSABLE ENTITY for invalid IDs.

        """
        response = client.get("/api/v1/pokemon/invalid")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = client.get("/api/v1/pokemon/-1")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = client.get("/api/v1/pokemon/0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
