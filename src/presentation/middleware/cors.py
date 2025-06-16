"""
CORS middleware configuration module.

Provides functionality to configure Cross-Origin Resource Sharing (CORS)
for the FastAPI application.
"""

from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings


def add_cors_middleware(app):
    """
    Add CORS middleware to FastAPI application.

    Configures permitted origins, methods, and headers for cross-origin requests
    based on application configuration.

    Args:
        app: FastAPI aplication instance

    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=settings.allow_credentials,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
    )
