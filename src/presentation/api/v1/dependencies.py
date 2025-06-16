"""
Provides dependency functions for FastAPI routes.

It includes:
- get_pokemon_api_client: Retrieves the PokeApiHttpClient instance from the application state.
- get_pokemon_by_id_use_case: Provides an instance of GetPokemonByIdUseCase
  with required dependencies.
"""

from fastapi import Depends, Request

from src.application.use_case.pokemon.get_pokemon_by_id import GetPokemonByIdUseCase
from src.infrastructure.service.pokeapi_client import PokeApiHttpClient


def get_pokemon_api_client(request: Request) -> PokeApiHttpClient:
    """
    Retrieve the PokeApiHttpClient instance from the FastAPI application state.

    Parameters
    ----------
    request : Request
        The FastAPI request object.

    Returns
    -------
    PokeApiHttpClient
        The PokeApiHttpClient instance.

    """
    return request.app.state.pokemon_api_client


def get_pokemon_by_id_use_case(
    pokemon_client: PokeApiHttpClient = Depends(get_pokemon_api_client),
) -> GetPokemonByIdUseCase:
    """
    Provide an instance of GetPokemonByIdUseCase with a PokeApiHttpClient dependency.

    Parameters
    ----------
    pokemon_client : PokeApiHttpClient
        The PokeApiHttpClient instance used to interact with the Pokemon API.

    Returns
    -------
    GetPokemonByIdUseCase
        An instance of GetPokemonByIdUseCase initialized with the provided PokeApiHttpClient.

    """
    return GetPokemonByIdUseCase(pokemon_api_client=pokemon_client)
