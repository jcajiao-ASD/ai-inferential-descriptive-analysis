"""
Provides the PokeApiHttpClient class for interacting with the PokeAPI.

The PokeApiHttpClient fetches Pokémon data from the PokeAPI and maps it to domain entities.
It includes methods for retrieving Pokémon by ID and managing the HTTP client session.
"""

import logging

import httpx

from src.application.interface.pokemon_api_client import PokemonApiClientInterface
from src.application.mappers.pokemon_mapper import PokemonMapper
from src.domain.entities.pokemon import Pokemon
from src.domain.exceptions.pokemon import PokemonNotFoundError


class PokeApiHttpClient(PokemonApiClientInterface):
    """
    A client for interacting with the PokeAPI.

    This class provides methods to fetch Pokémon data from the PokeAPI
    and map it to domain entities.

    Attributes
    ----------
    _client : httpx.AsyncClient
        The HTTP client used for making asynchronous requests.
    _base_url : str
        The base URL of the PokeAPI.
    _mapper : PokemonMapper
        The mapper used to transform API responses into domain entities.

    Methods
    -------
    get_pokemon_by_id(pokemon_id: int) -> Pokemon
        Fetch a Pokémon by its ID from the PokeAPI.
    close()
        Close the HTTP client session.

    """

    def __init__(self, client: httpx.AsyncClient):
        """
        Initialize the PokeApiHttpClient.

        Args:
            client (httpx.AsyncClient): The HTTP client to make asynchronous requests.
            base_url (str): The base URL of the PokeAPI. Defaults to "https://pokeapi.co/api/v2".

        """
        self._client = client
        self._mapper = PokemonMapper()

    async def get_pokemon_by_id(self, pokemon_id: int) -> Pokemon:
        """
        Fetch a Pokémon by its ID from the PokeAPI.

        Args:
            pokemon_id (int): The ID of the Pokémon to fetch.

        Returns:
            Pokemon: The Pokémon entity mapped from the API response.

        Raises:
            PokemonNotFoundError: If the Pokémon with the given ID is not found.
            httpx.HTTPStatusError: For HTTP errors other than 404.
            httpx.RequestError: For network-related errors.
            Exception: For any other unexpected errors.

        """
        url = f"/pokemon/{pokemon_id}"

        try:
            response = await self._client.get(url)
            response.raise_for_status()

            data = response.json()

            return self._mapper.from_pokeapi_response(data)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise PokemonNotFoundError(pokemon_id) from e

            logging.getLogger(__name__).error(f"HTTP error occurred: {e}")
            raise
        except httpx.RequestError as e:
            logging.getLogger(__name__).error(
                f"An error occurred while requesting {e.request.url!r}: {e}"
            )

            raise
        except Exception as e:
            logging.getLogger(__name__).error(f"An unexpected error occurred: {e}")
            raise

    async def close(self):
        """
        Close the HTTP client session.

        This method should be called to properly release resources
        associated with the HTTP client.
        """
        await self._client.aclose()
