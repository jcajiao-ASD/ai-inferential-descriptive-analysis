"""
Module for the GetPokemonByIdUseCase.

This module defines the use case for retrieving a Pokemon entity by its ID
using the PokemonApiClientInterface.
"""

from src.application.interface.pokemon_api_client import PokemonApiClientInterface
from src.domain.entities.pokemon import Pokemon


class GetPokemonByIdUseCase:

    """
    Use Case for obtaining a Pokemon by its ID.

    Orchestrates data retrieval from the external source
    (through the PokemonApiClientInterface)
    and returns the domain entity.
    """

    def __init__(self, pokemon_api_client: PokemonApiClientInterface):
        """
        Initialize the use case with a Pokemon API client.

        Args:
            pokemon_api_client: An instance of PokemonApiClientInterface to fetch Pokemon data.

        """
        self._pokemon_api_client = pokemon_api_client

    async def execute(self, pokemon_id: int) -> Pokemon:
        """
        Execute the use case to get the Pokemon.

        Args:
            pokemon_id: The ID of the Pokemon to retrieve.

        Returns:
            The corresponding Pokemon entity.

        Raises:
            PokemonNotFoundError: If the Pokemon is not found by the API client.

        """
        pokemon = await self._pokemon_api_client.get_pokemon_by_id(pokemon_id)

        return pokemon
