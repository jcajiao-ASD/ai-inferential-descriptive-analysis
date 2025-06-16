"""
Defines the application lifespan management for a FastAPI app.

It initializes and closes shared resources such as HTTP clients during the
application's startup and shutdown phases.
"""

import contextlib
import logging
from collections.abc import AsyncIterator

import httpx
from fastapi import FastAPI

from src.core.config import settings
from src.core.logging_setup import setup_logging
from src.infrastructure.service.pokeapi_client import PokeApiHttpClient


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the application lifecycle: startup and shutdown.

    Initialize and close shared resources such as HTTP clients.
    Resources are stored in app.state.
    """
    setup_logging()

    httpx_client_instance = httpx.AsyncClient(base_url=settings.poke_api_url)
    app.state.httpx_client = httpx_client_instance
    pokemon_api_client_instance = PokeApiHttpClient(client=httpx_client_instance)
    app.state.pokemon_api_client = pokemon_api_client_instance
    logging.getLogger(__name__).info("Lifespan setup complete. Application is ready.")

    yield

    if hasattr(app.state, "pokemon_api_client") and app.state.pokemon_api_client:
        await app.state.pokemon_api_client.close()

    logging.getLogger(__name__).info("Application shutdown complete.")
