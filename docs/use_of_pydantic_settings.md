### [<- back](_index.md)

#### Project - Insert project title
# Pydantic Settings

The following document explains the use of pydantic settings and the best practices related to this library.

<br>

## Document Contents

This document contains:

- **What is Pydantic?**
- **What is Pydantic Settings?**
- **As used within the example?**

<br>

# What is Pydantic?

Pydantic is a powerful Python library used primarily for data validation and data modeling. It allows you to define how your data should look using standard Python type hints. Pydantic automatically validates incoming data against these definitions and provides clear errors if the data doesn't match the expected structure or types. It's widely used in FastAPI for request body validation, response serialization, and also for settings management.

<br><br>

# What is Pydantic Settings?

Pydantic Settings is an extension of the core Pydantic library specifically designed to simplify loading application configuration settings. Instead of manually reading environment variables using os.getenv() everywhere, Pydantic Settings allows you to define your configuration structure using a Pydantic model and automatically load values from:

Environment variables (the primary source).
.env files (convenient for local development).
Other sources like secrets or configuration files.
It provides a structured, type-annotated, and validated way to manage your application's configuration based on the environment it's running in.

<br><br>

# As used within the example?

In this project, Pydantic Settings is used to centralize and manage application configuration loaded from environment variables and the .env file.

<br>

## Defining the Configuration (src/core/config.py)
The main configuration is defined in src/core/config.py.

```python

# src/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # CORS settings with defaults
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = False
    allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    allow_headers: list[str] = ["*"]

    # Example of a setting without a default (required)
    poke_api_url: str

    # LOGS
    logs_file_name: str = "app.log"

    # This configuration tells Pydantic Settings how to load values
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Create a single instance of the Settings object
# This happens when the config.py module is first imported.
# Pydantic Settings loads from environment variables and the .env file here.
settings = Settings()

```

<br>

- The Settings class inherits from BaseSettings, indicating it's a configuration model.
- Each attribute (like poke_api_url, allow_origins) represents a configuration variable with a specific type (like str, list[str]).
- Attributes with = value define a default value if the setting isn't found in environment variables or the .env file.
- model_config = SettingsConfigDict(...) tells Pydantic Settings to look for a file named .env and load variables from it (in addition to standard environment variables, which have higher priority).
- The settings = Settings() line creates the actual Settings object by reading the environment and the .env file, validating the data, and populating the object's attributes. This object is typically created once when the config.py module is first imported during application startup.

<br>

## Using the Configuration in the Application

Once the settings object is created in config.py, other parts of the application can import and use it to access configuration values.

```python

# src/core/lifespan/app_lifespan.py (Example Usage)

"""
Defines the application lifespan management...
"""
import contextlib
from collections.abc import AsyncIterator
import httpx
from fastapi import FastAPI
from src.core.config import settings # <-- The settings object is imported here
from src.infrastructure.service.pokeapi_client import PokeApiHttpClient

@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    # ... other lifespan code ...

    # Accessing the loaded configuration for the base URL
    httpx_client_instance = httpx.AsyncClient(base_url=settings.poke_api_url) # <-- settings.poke_api_url is used here
    pokemon_api_client_instance = PokeApiHttpClient(client=httpx_client_instance, base_url=settings.poke_api_url) # And here

    # ... rest of lifespan setup ...

    yield

    # ... shutdown ...

```