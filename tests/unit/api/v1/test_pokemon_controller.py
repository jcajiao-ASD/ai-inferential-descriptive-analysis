"""
Unit tests for the Pokemon Controller API endpoints.

This module contains tests that verify the behavior of the Pokemon API endpoints
in isolation, using mocks for dependencies such as use cases and services.
Tests verify correct HTTP responses, status codes, and JSON formatting
for various scenarios including successful requests and error handling.
"""

from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status
from src.domain.entities.pokemon import Pokemon
from src.domain.exceptions.pokemon import PokemonNotFoundError
from src.presentation.api.v1.pokemon_controller import get_pokemon_by_id_endpoint


@pytest.fixture
def mock_get_pokemon_by_id_use_case():
    """Create a mock for the GetPokemonByIdUseCase."""
    return AsyncMock()


@pytest.fixture
def mock_response():
    """Create a mock for the FastAPI response object."""
    return AsyncMock()


@pytest.mark.asyncio
class TestGetPokemonByIdEndpoint:
    
    """Tests for the get_pokemon_by_id_endpoint function."""

    async def test_get_pokemon_by_id_success(
        self,
        mock_get_pokemon_by_id_use_case,
        mock_response,
    ):
        """Test successful retrieval of a Pokemon by ID."""
        # Arrange
        pokemon_id = 25
        expected_pokemon = Pokemon(id=pokemon_id, name="pikachu", types=["electric"])
        mock_get_pokemon_by_id_use_case.execute.return_value = expected_pokemon
        mock_response.headers = {}

        # Act
        result = await get_pokemon_by_id_endpoint(
            pokemon_id=pokemon_id, use_case=mock_get_pokemon_by_id_use_case, response=mock_response
        )

        # Assert
        assert result == expected_pokemon
        mock_get_pokemon_by_id_use_case.execute.assert_called_once_with(pokemon_id=pokemon_id)
        assert mock_response.headers["Cache-Control"] == "public, max-age=3600"

    async def test_get_pokemon_by_id_not_found(
        self,
        mock_get_pokemon_by_id_use_case,
        mock_response,
    ):
        """Test handling of PokemonNotFoundError by returning a 404 HTTPException."""
        # Arrange
        pokemon_id = 9999
        mock_get_pokemon_by_id_use_case.execute.side_effect = PokemonNotFoundError(
            f"Pokemon with ID {pokemon_id} not found"
        )
        mock_response.headers = {}

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_pokemon_by_id_endpoint(
                pokemon_id=pokemon_id,
                use_case=mock_get_pokemon_by_id_use_case,
                response=mock_response,
            )

        # Verify exception details
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert f"Pokemon with ID {pokemon_id} not found" in exc_info.value.detail

    async def test_get_pokemon_by_id_unexpected_error(
        self,
        mock_get_pokemon_by_id_use_case,
        mock_response,
    ):
        """Test handling of unexpected exceptions by returning a 500 HTTPException."""
        # Arrange
        pokemon_id = 25
        mock_get_pokemon_by_id_use_case.execute.side_effect = Exception("Unexpected error")
        mock_response.headers = {}

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_pokemon_by_id_endpoint(
                pokemon_id=pokemon_id,
                use_case=mock_get_pokemon_by_id_use_case,
                response=mock_response,
            )

        # Verify exception details
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "An internal server error occurred" in exc_info.value.detail
