"""
Define the interface for interacting with external Pokemon data sources.

Provide an abstract base class, `PokemonApiClientInterface`, which specifies
the contract that any concrete implementation of a Pokemon API client must fulfill.
"""

from abc import ABC, abstractmethod

from src.domain.entities.pokemon import Pokemon


class PokemonApiClientInterface(ABC):

    """
    Interface defining the contract for Pokemon API client implementations.
    
    This abstract class establishes the methods that any concrete Pokemon API
    client must implement to interact with external Pokemon data sources.
    """
    
    @abstractmethod
    async def get_pokemon_by_id(self, pokemon_id: int) -> Pokemon:
        """
        Get a Pokemon by its ID.

        Args:
            pokemon_id: The numeric ID of the Pokemon.

        Returns:
            An instance of the Pokemon entity.

        Raises:
            PokemonNotFoundException: If the Pokemon with the given ID is not found.
            # Could raise other infrastructure exceptions if necessary,
            # but ideally, infrastructure exceptions are translated to domain
            # or application exceptions in the concrete implementation.

        """
