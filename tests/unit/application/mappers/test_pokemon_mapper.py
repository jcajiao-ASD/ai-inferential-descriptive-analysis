"""
Unit tests for the PokemonMapper class.

This module contains tests to verify that the PokemonMapper correctly
transforms external API responses into domain Pokemon entities.
"""

from src.application.mappers.pokemon_mapper import PokemonMapper
from src.domain.entities.pokemon import Pokemon


class TestPokemonMapper:

    """Tests for the PokemonMapper class methods."""

    def test_from_pokeapi_response_with_valid_data(self):
        """Test mapping from a valid and complete PokeAPI response."""
        # Arrange
        pokeapi_data = {
            "id": 25,
            "name": "pikachu",
            "types": [
                {"type": {"name": "electric"}},
            ],
        }

        # Act
        result = PokemonMapper.from_pokeapi_response(pokeapi_data)

        # Assert
        assert isinstance(result, Pokemon)
        assert result.id == 25
        assert result.name == "pikachu"
        assert result.types == ["electric"]

    def test_from_pokeapi_response_with_multiple_types(self):
        """Test mapping from a response with multiple Pokemon types."""
        # Arrange
        pokeapi_data = {
            "id": 6,
            "name": "charizard",
            "types": [
                {"type": {"name": "fire"}},
                {"type": {"name": "flying"}},
            ],
        }

        # Act
        result = PokemonMapper.from_pokeapi_response(pokeapi_data)

        # Assert
        assert result.types == ["fire", "flying"]

    def test_from_pokeapi_response_with_missing_types(self):
        """Test mapping from a response without the 'types' field."""
        # Arrange
        pokeapi_data = {
            "id": 1,
            "name": "bulbasaur",
        }

        # Act
        result = PokemonMapper.from_pokeapi_response(pokeapi_data)

        # Assert
        assert result.id == 1
        assert result.name == "bulbasaur"
        assert result.types == []

    def test_from_pokeapi_response_with_malformed_types(self):
        """Test mapping from a response with malformed type data."""
        # Arrange
        pokeapi_data = {
            "id": 150,
            "name": "mewtwo",
            "types": [
                {"not_type": {"name": "psychic"}},
                {"type": "malformed"},
                {"type": {"not_name": "psychic"}},
                {"type": {"name": "psychic"}},
            ],
        }

        # Act
        result = PokemonMapper.from_pokeapi_response(pokeapi_data)

        # Assert
        assert result.types == ["psychic"]

    def test_from_pokeapi_response_with_empty_data(self):
        """Test mapping from an empty response."""
        # Arrange
        pokeapi_data = {}

        # Act
        result = PokemonMapper.from_pokeapi_response(pokeapi_data)

        # Assert
        assert result.id is None
        assert result.name is None
        assert result.types == []
