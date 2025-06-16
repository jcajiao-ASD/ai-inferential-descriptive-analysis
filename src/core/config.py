"""
Configuration module for the application.

This module defines the `Settings` class, which loads and manages
environment-based configuration settings for the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes
    ----------
    allow_origins : list[str]
        List of allowed origins for CORS.
    allow_credentials : bool
        Whether to allow credentials in CORS.
    allow_methods : list[str]
        List of allowed HTTP methods for CORS.
    allow_headers : list[str]
        List of allowed headers for CORS.
    poke_api_url : str
        The base URL for the Pokémon API.

    """

    # CORS
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = False
    allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    allow_headers: list[str] = ["*"]

    # LOGS
    logs_file_name: str = "app.log"

    # POKE API
    poke_api_url: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
