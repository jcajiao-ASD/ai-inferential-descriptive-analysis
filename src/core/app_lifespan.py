"""
Defines the application lifespan management for a FastAPI app.

It initializes and closes shared resources during the
application's startup and shutdown phases.
"""

import contextlib
import logging
from collections.abc import AsyncIterator

from fastapi import FastAPI

from src.core.logging_setup import setup_logging


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the application lifecycle: startup and shutdown.

    Initialize and close shared resources.
    """
    setup_logging()
    logging.getLogger(__name__).info("Lifespan setup complete. Application is ready.")

    yield

    logging.getLogger(__name__).info("Application shutdown complete.")
