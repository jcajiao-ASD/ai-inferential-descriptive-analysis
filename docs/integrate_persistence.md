### [<- back](_index.md)

#### Project - Insert project title
# Integrate Persistence

The following document contains information on how to integrate persistence using the Clean Architecture and RestAPI architectural pattern. It will also discuss concurrency management.

<br>

## Document Contents

This document contains:

- **Practices to avoid concurrency problems**
- **Code example**

<br><br>

# Practices to avoid concurrency problems
When you integrate data persistence, especially databases, you introduce a shared resource that multiple concurrent requests will try to access and modify. While FastAPI/Uvicorn are great at managing concurrent waits, they don't automatically solve problems with shared mutable data.

Here are practices to handle concurrency related to persistence:

- **Connection Pooling**: Configure your database client or driver to use a connection pool. This is managed in the `lifespan` function (Step 5). Instead of opening a new connection for every request, concurrent requests share a pool of ready connections, which is much more efficient under load.

- **Asynchronous Drivers**: Use database drivers and clients specifically designed for asynchronous Python (like `motor` for MongoDB, `asyncpg` for PostgreSQL, `aioredis` for Redis). These drivers integrate with `asyncio's` event loop, allowing your application to perform other tasks while waiting for database operations to complete, preventing your application processes from blocking.

- **Transactions**: Use database transactions (managed within your Infrastructure/Repository implementation) to group related read and write operations. Transactions ensure that a sequence of operations is treated as a single atomic unit – either all succeed or none do (`COMMIT` or `ROLLBACK`). This is fundamental for data consistency.

- **Isolation Levels**: Understand and select the appropriate transaction isolation level for your database. Isolation levels determine how transactions interact with each other. Higher levels (like `Repeatable Read` or `Serializable`) prevent logical concurrency problems (like "read-modify-write" race conditions) but can reduce concurrency. Use these for critical operations where the outcome depends on reading the current state before writing.

- **Atomic Operations**: Whenever possible, use database-native atomic operations (e.g., incrementing a counter directly in SQL: `UPDATE table SET count = count + 1 WHERE ...).` These operations are designed by the database to be safe even with multiple concurrent attempts.

- **Idempotency**: Design your operations (especially write operations) to be idempotent if possible. An idempotent operation can be performed multiple times with the same effect as performing it once. This is helpful for retries in a distributed/concurrent system.

- **Concurrency in Redis/Messaging**: Redis is mostly single-threaded but handles many concurrent connections efficiently via its event loop. Message queues like RabbitMQ handle concurrency by having multiple consumers processing messages independently. Understand the concurrency model of the specific persistence tool you use.

<br>

By combining the architectural separation of concerns with proper concurrency management techniques for your chosen persistence solution, you can build a reliable and scalable application.

<br><br>

# Code example

Below are code snippets demonstrating how the persistence integration steps described previously translate into actual Python code within the scaffold's structure. We will use MongoDB with the motor driver as the example persistence solution and illustrate the process for a User entity.

<br>

- **Step 1**: Define the Core Business Entity (Domain Layer)

This code defines the core User entity using Python's dataclasses. It represents the user concept in the pure business domain, holding data like id, username, and email, independent of any database or framework details.


```python

# src/domain/entities/user.py

from uuid import UUID
from dataclasses import dataclass


@dataclass
class User:
    id: UUID
    username: str
    email: str

```

<br>

- **Step 2**: Define Domain Exceptions related to the entity

This code defines custom exceptions for business problems specifically related to users. UserNotFoundException is used when a user cannot be found (a domain-level issue), and DuplicateUsernameException signals a business rule violation if a username already exists. These exceptions are also part of the pure Domain layer.

```python

# src/domain/exceptions/user.py

import uuid

class UserNotFoundException(Exception):
    def __init__(self, identifier: str | uuid.UUID):
        self.identifier = identifier
        super().__init__(f"User with identifier '{identifier}' not found.")

class DuplicateUsernameException(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User with username '{username}' already exists.")

```

<br>

- **Step 3**: Define the Repository Interface (Application Layer)

This code defines the UserRepositoryInterface. It's an abstract contract (a Port) in the Application layer, specifying the essential data operations that the Application layer needs for User entities. It does not contain any implementation details, ensuring the Application layer depends only on this contract.

```python

# src/application/interface/user_repository.py

from abc import ABC, abstractmethod
import uuid
from src.domain.entities.user import User

class UserRepositoryInterface(ABC):

    @abstractmethod
    async def add(self, user: User) -> None:
        pass

```

<br>

- **Step 4**: Create User mapper

This code defines the UserMapper class. Located in the Application layer's mappers directory, its purpose is to handle the conversion of data between the pure User Domain entity format and other formats, specifically the dictionary format (dict) used to represent a document in MongoDB.

```python

# src/application/mappers/user_mapper.py

import uuid
from src.domain.entities.user import User


class UserMapper:
    @staticmethod
    def user_to_document(user: User) -> dict:
        return {"_id": str(user.id), "username": user.username, "email": user.email}

    @staticmethod
    def document_to_user(document: dict) -> User:
        return User(
            id=uuid.UUID(document["_id"]), username=document["username"], email=document["email"]
        )

```

<br>

- **Step 5**: Use the Repository in Your Application Logic (Application Layer)

This code shows the CreateUserUseCase. This Use Case, part of the Application layer, contains the specific logic for the "create user" feature. It depends on the UserRepositoryInterface (defined in Step 3) to perform persistence operations. The code demonstrates how the Use Case calls the add method on its injected user_repository dependency (which is an object implementing the interface) and handles a potential DuplicateUsernameException.

```python

# src/application/use_case/user/create_user.py

import uuid
from src.domain.entities.user import User
from src.domain.exceptions.user import DuplicateUsernameException
from src.application.interface.user_repository import UserRepositoryInterface


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository

    async def execute(self, username: str, email: str) -> User:

        new_user_id = uuid.uuid4()
        new_user = User(id=new_user_id, username=username, email=email)

        await self._user_repository.add(new_user)

        return new_user

```

<br>

- **Step 6**: Create factory for mongo client:

This code defines the create_mongo_client factory function. Located in the Infrastructure layer's database directory, its specific job is to encapsulate the detail of how to create an instance of the motor.motor_asyncio.AsyncIOMotorClient (the low-level MongoDB driver). This function is used by the Core layer during application startup.

```python

# src/infrastructure/database/mongo_client_factory.py

from motor import motor_asyncio

async def create_mongo_client(connection_string: str) -> motor_asyncio.AsyncIOMotorClient:
    client = motor_asyncio.AsyncIOMotorClient(connection_string)
    return client

```

<br>


- **Step 7**: Implement the Concrete Repository (Infrastructure Layer)

This code defines the MongoUserRepository class. Located in the Infrastructure layer, it implements the UserRepositoryInterface contract (defined in Step 3). This class contains the technical logic for interacting with MongoDB using a motor.motor_asyncio.AsyncIOMotorClient instance (obtained via the factory in Step 6) and uses the UserMapper (from Step 4) to convert data when reading from or writing to the database.

```python

# src/infrastructure/repository/mongo_user_repository.py

from motor import motor_asyncio
from src.application.interface.user_repository import UserRepositoryInterface
from src.application.mappers.user_mapper import UserMapper
from src.domain.entities.user import User

class MongoUserRepository(UserRepositoryInterface):

    def __init__(
        self,
        mongo_client: motor_asyncio.AsyncIOMotorClient,
        db_name: str,
        collection_name: str,
    ):
        self._client = mongo_client
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]
        self._mapper = UserMapper()


    async def add(self, user: User) -> None:
        document = self._mapper.user_to_document(user)
        try:
            await self._collection.insert_one(document)
        except DuplicateKeyError as e:
            raise DuplicateUsernameException(username=user.username) from e
        except Exception as e:
            print(f"Error adding user {user.id}: {e}")
            raise

```

<br>

- **Step 8**: Create environment variables

This section shows the content of the .env file. This file, located at the project root, defines environment-specific configuration values as key-value pairs, such as database connection strings and API URLs. These values are loaded by the configuration system during application startup.

```

# --- Database Configuration ---
MONGO_CONNECTION="mongodb://localhost:27017"
MONGO_DATABASE_NAME="mydatabase"
MONGO_USER_COLLECTION="users"
MONGO_PRODUCT_COLLECTION="products"


# --- others variables ---

```

<br>

- **Step 9**: Add configurations to the core layer's config.py

This code defines the Settings model using Pydantic Settings in the core layer's config.py file. This class specifies the expected structure and types for the application's configuration. It is configured (model_config) to load values automatically from environment variables and the .env file (from Step 8), providing a centralized, typed configuration object (settings) for the application.

```python

# src/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    # ** CONFIG POKEAPI **
    
    poke_api_url: str

    # ** CONFIG DATABASE **

    mongo_connection: str
    mongo_database_name: str
    mongo_user_collection: str
    mongo_product_collection: str

    # ** CONFIG CORS **

    allow_origins: list[str] = ["*"]
    allow_credentials: bool = False
    allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    allow_headers: list[str] = ["*"]

    # ** CONFIG .ENV FILE **

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

```

<br>


- **Step 10**: Set Up and Wire the Database Connection (Core Layer)

This code shows additions to the app_lifespan function. Located in the core layer, this function is part of the application's startup process. It uses the settings object (from Step 9) to get configuration values. It calls the create_mongo_client factory (from Step 6) to get the MongoDB client instance and creates the MongoUserRepository instance (from Step 7), injecting the MongoDB client and names from settings into the repository. It then stores these instances in app.state, making them available for dependency injection in outer layers, and ensures they are closed on shutdown.


```python

# src/core/lifespan/app_lifespan.py

import contextlib
from collections.abc import AsyncIterator
import httpx
from fastapi import FastAPI
from src.core.config import settings
from src.infrastructure.database.mongo_client_factory import create_mongo_client
from src.infrastructure.repository.mongo_user_repository import MongoUserRepository
from src.infrastructure.service.pokeapi_client import PokeApiHttpClient


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:

    httpx_client_instance = httpx.AsyncClient()
    pokemon_api_client_instance = PokeApiHttpClient(
        client=httpx_client_instance, base_url=settings.poke_api_url
    )

    app.state.httpx_client = httpx_client_instance
    app.state.pokemon_api_client = pokemon_api_client_instance

    mongo_client_instance = await create_mongo_client(settings.mongo_connection)

    user_repository_instance = MongoUserRepository(
        mongo_client=mongo_client_instance,
        db_name=settings.mongo_database_name,
        collection_name=settings.mongo_user_collection,
    )

    app.state.user_repository = user_repository_instance
    app.state.mongo_client = mongo_client_instance

    try:
        await app.state.mongo_client.admin.command('ping')
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

    yield

    if hasattr(app.state, "pokemon_api_client") and app.state.pokemon_api_client:
        await app.state.pokemon_api_client.close()

    if hasattr(app.state, "mongo_client") and app.state.mongo_client:
        app.state.mongo_client.close()

```

<br>


- **Step 11**: Provide the Repository and Use Cases for Injection (Presentation Layer)

This code shows additions to the dependencies.py file, located in the Presentation layer's API package. It defines FastAPI dependency provider functions (like get_user_repository, create_user_use_case, get_user_by_id_use_case). These functions access the resource instances stored in app.state during the lifespan (Step 10) and provide them to endpoint functions using FastAPI.Depends.

```python

# src/presentation/api/v1/dependencies.py

from fastapi import Depends, Request
from src.application.interface.user_repository import UserRepositoryInterface
from src.application.use_case.pokemon.get_pokemon_by_id import GetPokemonByIdUseCase
from src.application.use_case.user.create_user import CreateUserUseCase
from src.infrastructure.service.pokeapi_client import PokeApiHttpClient


def get_pokemon_api_client(request: Request) -> PokeApiHttpClient:
    return request.app.state.pokemon_api_client


def get_pokemon_by_id_use_case(
    pokemon_client: PokeApiHttpClient = Depends(get_pokemon_api_client),
) -> GetPokemonByIdUseCase:
    return GetPokemonByIdUseCase(pokemon_api_client=pokemon_client)


def get_user_repository(request: Request) -> UserRepositoryInterface:
    return request.app.state.user_repository


def create_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository=user_repository)

```

<br>

- **Step 12**: Create models with pydantic and Create API Endpoints (Presentation Layer)

This code defines Pydantic schemas for validating incoming request bodies (UserCreateRequest) and structuring outgoing responses (UserResponse), and shows a FastAPI endpoint (create_user_endpoint) in the Presentation layer's user_controller.py. The endpoint uses Annotated and Depends (linking to providers in Step 11) to receive the CreateUserUseCase dependency. It validates the request body, calls the Use Case, and handles Domain Exceptions by translating them into appropriate HTTP responses.


```python

# src/presentation/models/v1/user_schemas.py

import uuid
from pydantic import BaseModel, Field, EmailStr


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

```

<br>


```python

# src/presentation/api/v1/user/user_controller.py

from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status
from src.application.use_case.user.create_user import CreateUserUseCase
from src.domain.exceptions.user import DuplicateUsernameException
from src.presentation.api.v1.dependencies import (
    create_user_use_case,
)
from src.presentation.schemas.v1.user_schemas import UserCreateRequest, UserResponse

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new User",
)
async def create_user_endpoint(
    use_case: Annotated[CreateUserUseCase, Depends(create_user_use_case)],
    user_data: Annotated[UserCreateRequest, Body(...)],
):
    try:
        created_user = await use_case.execute(username=user_data.username, email=user_data.email)

        return created_user

    except DuplicateUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Username '{e.username}' already exists."
        ) from e
    except Exception as e:
        print(f"An unexpected error occurred in create user endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred.",
        ) from e

```

<br>


- **Step 13**: Update Main Entry Point

This code shows additions to the main.py file. This is the application's entry point. It is responsible for assembling the top-level components, including creating the FastAPI app instance, attaching the lifespan function (from Step 10), adding middleware, and including the routers (like the user_controller.router from Step 12) to make the endpoints accessible.

```python

# main.py

"""FastAPI Application Entry Point."""

from fastapi import FastAPI
from src.core.lifespan.app_lifespan import app_lifespan
from src.presentation.api.healthcheck import healthcheck_router
from src.presentation.api.v1 import pokemon_controller, user_controller
from src.presentation.middleware.cors import add_cors_middleware

app = FastAPI(
    title="Domain services - Project",
    description="Description services",
    version="0.0.1",
    contact={
        "name": "Grupo ASD S.AS.",
        "url": "https://www.grupoasd.com/contacto/",
    },
    lifespan=app_lifespan,
)

add_cors_middleware(app)

app.include_router(healthcheck_router.router, tags=["healthcheck"], prefix="/api")
app.include_router(pokemon_controller.router, tags=["pokemon"], prefix="/api/v1/pokemon")
app.include_router(user_controller.router, tags=["user"], prefix="/api/v1/user")


```
