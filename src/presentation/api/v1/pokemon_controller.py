"""
Defines the Pokémon controller for the FastAPI application.

It includes the endpoint to retrieve Pokémon data by ID, leveraging the
GetPokemonByIdUseCase and handling exceptions such as PokemonNotFoundError.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status

from src.application.use_case.pokemon.get_pokemon_by_id import GetPokemonByIdUseCase
from src.domain.entities.pokemon import Pokemon
from src.domain.exceptions.pokemon import PokemonNotFoundError
from src.presentation.api.v1.dependencies import get_pokemon_by_id_use_case

router = APIRouter()


@router.get(
    "/{pokemon_id}",
    response_model=Pokemon,
    summary="Get a Pokémon by ID",
    description="Retrieve a specific Pokémon's data from PokeAPI by its ID.",
)
async def get_pokemon_by_id_endpoint(
    pokemon_id: Annotated[int, Path(..., gt=0)],
    use_case: Annotated[GetPokemonByIdUseCase, Depends(get_pokemon_by_id_use_case)],
    response: Response,
):
    """
    Retrieve a Pokémon's data by its ID.

    Parameters
    ----------
    pokemon_id : int
        The ID of the Pokémon to retrieve. Must be greater than 0.
    use_case : GetPokemonByIdUseCase
        The use case instance to handle the retrieval logic.
    response: Response
        The response object to set custom headers.
        The response object to set custom headers.

    Returns
    -------
    Pokemon
        The Pokémon entity corresponding to the given ID.

    Raises
    ------
    HTTPException
        If the Pokémon is not found (404) or if an internal server error occurs (500).

    """
    try:
        pokemon = await use_case.execute(pokemon_id=pokemon_id)
        response.headers["Cache-Control"] = "public, max-age=3600"
        return pokemon

    except PokemonNotFoundError as e:
        logging.getLogger(__name__).error(f"Pokemon with ID {pokemon_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Pokemon with ID {pokemon_id} not found."
        ) from e
    except Exception as e:
        logging.getLogger(__name__).error(f"An unexpected error occurred in endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred.",
        ) from e
