"""
Unit tests for the GetPokemonByIdUseCase.

This module contains tests to verify that the use case correctly
retrieves Pokemon entities by ID through the Pokemon API client.
"""

from unittest.mock import AsyncMock

import pytest
from src.application.use_case.pokemon.get_pokemon_by_id import GetPokemonByIdUseCase
from src.domain.entities.pokemon import Pokemon
from src.domain.exceptions.pokemon import PokemonNotFoundError


@pytest.fixture
def mock_pokemon_api_client():
    """Create a mock for the PokemonApiClientInterface."""
    return AsyncMock()


@pytest.fixture
def use_case(mock_pokemon_api_client):
    """Create a GetPokemonByIdUseCase instance with a mock API client."""
    return GetPokemonByIdUseCase(pokemon_api_client=mock_pokemon_api_client)


class TestGetPokemonByIdUseCase:

    """Tests for the GetPokemonByIdUseCase class."""

    @pytest.mark.asyncio
    async def test_execute_returns_pokemon_when_found(self, use_case, mock_pokemon_api_client):
        """Test that execute returns the Pokemon when found by the API client."""
        # Arrange
        pokemon_id = 25
        expected_pokemon = Pokemon(id=pokemon_id, name="pikachu", types=["electric"])
        mock_pokemon_api_client.get_pokemon_by_id.return_value = expected_pokemon

        # Act
        result = await use_case.execute(pokemon_id=pokemon_id)

        # Assert
        assert result == expected_pokemon
        mock_pokemon_api_client.get_pokemon_by_id.assert_called_once_with(pokemon_id)

    @pytest.mark.asyncio
    async def test_execute_passes_pokemon_id_to_api_client(self, use_case, mock_pokemon_api_client):
        """Test that execute passes the correct pokemon_id to the API client."""
        # Arrange
        pokemon_id = 150
        mock_pokemon_api_client.get_pokemon_by_id.return_value = Pokemon(
            id=pokemon_id, name="mewtwo", types=["psychic"]
        )

        # Act
        await use_case.execute(pokemon_id=pokemon_id)

        # Assert
        mock_pokemon_api_client.get_pokemon_by_id.assert_called_once_with(pokemon_id)

    @pytest.mark.asyncio
    async def test_execute_propagates_not_found_error(self, use_case, mock_pokemon_api_client):
        """Test that execute propagates PokemonNotFoundError from the API client."""
        # Arrange
        pokemon_id = 9999
        mock_pokemon_api_client.get_pokemon_by_id.side_effect = PokemonNotFoundError(
            f"Pokemon with ID {pokemon_id} not found"
        )

        # Act & Assert
        with pytest.raises(PokemonNotFoundError) as exc_info:
            await use_case.execute(pokemon_id=pokemon_id)

        assert f"Pokemon with ID {pokemon_id} not found" in str(exc_info.value)
        mock_pokemon_api_client.get_pokemon_by_id.assert_called_once_with(pokemon_id)
