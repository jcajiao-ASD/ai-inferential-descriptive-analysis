### [<- back](_index.md)

#### Project - Insert project title
# Explanation Testing Example

This document explains how to create a unit test for an application use case and also an integration test for an endpoint.

<br>

## Document Contents

This document contains:

- Use case unit testing
- Endpoint integration testing

<br><br>

# Use Case Unit Testing

This code is a unit test for the `GetPokemonByIdUseCase` class, testing its behavior in isolation.

```python

# Unit test code snippet
"""
Unit tests for the GetPokemonByIdUseCase.
...
"""
from unittest.mock import AsyncMock
import pytest
from src.application.use_case.pokemon.get_pokemon_by_id import GetPokemonByIdUseCase
from src.domain.entities.pokemon import Pokemon
from src.domain.exceptions.pokemon import PokemonNotFoundError


@pytest.fixture
def mock_pokemon_api_client():
    """Create a mock for the PokemonApiClientInterface."""
    return AsyncMock()


@pytest.fixture
def use_case(mock_pokemon_api_client):
    """Create a GetPokemonByIdUseCase instance with a mock API client."""
    # This injects the mock into the Use Case (the code being tested)
    return GetPokemonByIdUseCase(pokemon_api_client=mock_pokemon_api_client)


class TestGetPokemonByIdUseCase:
    """Tests for the GetPokemonByIdUseCase class."""

    @pytest.mark.asyncio
    async def test_execute_returns_pokemon_when_found(self, use_case, mock_pokemon_api_client):
        """Test that execute returns the Pokemon when found by the API client."""
        # Arrange: Set up input, expected output, and configure the mock
        pokemon_id = 25
        expected_pokemon = Pokemon(id=pokemon_id, name="pikachu", types=["electric"])
        # Tell the mock's method what to return when called by the Use Case
        mock_pokemon_api_client.get_pokemon_by_id.return_value = expected_pokemon

        # Act: Execute the Use Case method being tested
        result = await use_case.execute(pokemon_id=pokemon_id)

        # Assert: Verify the outcome and dependency interaction
        # Check that the Use Case returned the expected result
        assert result == expected_pokemon
        # Verify that the Use Case called its dependency's method correctly
        mock_pokemon_api_client.get_pokemon_by_id.assert_called_once_with(pokemon_id)


```

Explanation:

This test verifies the GetPokemonByIdUseCase specifically when its external dependency (the API client) successfully finds and returns a Pokémon.


1. Fixtures `(mock_pokemon_api_client, use_case)`: They set up the test environment.

    - mock_pokemon_api_client creates a simulated client (AsyncMock) that stands in for the real PokemonApiClientInterface implementation.
    - use_case creates an instance of GetPokemonByIdUseCase and injects this mock client into it. This isolates the Use Case logic.

2. Test Method (test_execute_returns_pokemon_when_found): This is the actual test case.

    - **Arrange**: It prepares the test by defining the input ID and the expected Pokemon object. Crucially, it tells the mock_pokemon_api_client to return this expected Pokémon when its get_pokemon_by_id method is called.
    - **Act**: It runs the Use Case's execute method with the test input. The Use Case will internally call its dependency (self._pokemon_api_client.get_pokemon_by_id), which is the mock.
    - **Assert**: It checks two things:
        - Did the Use Case's execute method return the correct Pokemon object? (It should return what the mock returned).
        - Did the Use Case's execute method actually call its dependency (mock_pokemon_api_client.get_pokemon_by_id) exactly once and with the correct input ID?

In Summary:

This unit test confirms that the GetPokemonByIdUseCase correctly handles the successful response from its dependency and interacts with that dependency as expected. It isolates the Use Case's logic from the actual external API call.

<br><br>

# Endpoint integration testing

This code snippet shows how to write an integration test for a FastAPI endpoint using pytest and unittest.mock. The goal is to test the flow from a simulated HTTP request through parts of the application layers, using a mock for an external dependency.

```python

from collections.abc import Generator
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from src.domain.entities.pokemon import Pokemon
from src.domain.exceptions.pokemon import PokemonNotFoundError
from src.infrastructure.service.pokeapi_client import PokeApiHttpClient
from src.presentation.api.v1.dependencies import get_pokemon_api_client


@pytest.fixture(scope="session")
def app() -> FastAPI:
    from main import app as fastapi_app
    return fastapi_app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_pokemon_api_client(client: TestClient):
    mock_client_instance = AsyncMock(spec_async=PokeApiHttpClient)

    def override_get_pokemon_api_client_provider():
        return mock_client_instance

    client.app.dependency_overrides[get_pokemon_api_client] = (
        override_get_pokemon_api_client_provider
    )

    yield mock_client_instance

    del client.app.dependency_overrides[get_pokemon_api_client]


@pytest.fixture
def override_pokemon_api_client_dependency(
    client: TestClient, mock_pokemon_api_client_instance: AsyncMock
):

    def override_get_pokemon_api_client():
        return mock_pokemon_api_client_instance

    client.app.dependency_overrides[get_pokemon_api_client] = override_get_pokemon_api_client

    yield mock_pokemon_api_client_instance

    del client.app.dependency_overrides[get_pokemon_api_client]


class TestPokemonController:

    def test_get_pokemon_by_id_success(
        self, client: TestClient, mock_pokemon_api_client: AsyncMock
    ):
        pokemon_id = 25
        expected_pokemon = Pokemon(id=pokemon_id, name="pikachu", types=["electric"])

        mock_pokemon_api_client.get_pokemon_by_id.return_value = expected_pokemon

        response = client.get(f"/api/v1/pokemon/{pokemon_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": pokemon_id, "name": "pikachu", "types": ["electric"]}
        assert "Cache-Control" in response.headers
        assert response.headers["Cache-Control"] == "public, max-age=3600"

        mock_pokemon_api_client.get_pokemon_by_id.assert_called_once_with(pokemon_id)

```

**Explanation:**

1. Fixtures (app, client): These set up the test environment.
    - app: Provides FastAPI application instance itself.
    - client: Provides TestClient, a tool to make simulated HTTP requests against app directly in memory.

2. Mock Fixture (mock_pokemon_api_client): This fixture is key for controlling dependencies.
    - It creates an AsyncMock object that acts as a stand-in for real PokeApiHttpClient (the external dependency handler).
    - Crucially, it uses FastAPI's dependency_overrides feature (client.app.dependency_overrides[...]) to tell the application: "For this test, whenever someone asks for the real Pokemon API client (via its dependency provider), give them this mock instead."

3. test_get_pokemon_by_id_success Test: This specific test case verifies the endpoint works correctly in a successful scenario.

    - `Arrange`: Sets up the test data, including the pokemon_id and the Pokemon object expected as a result. It then configures the mock_pokemon_api_client to return this specific Pokemon object when its get_pokemon_by_id method is called by the Use Case.

    - `Act`: It uses the client to make a simulated GET request to the endpoint's URL (/api/v1/pokemon/25). This triggers the FastAPI request handling flow, including dependency injection (which now uses the mock) and executing endpoint/Use Case code.

    - `Assert`: It checks that the simulated HTTP response is correct (status code 200, expected JSON body, expected cache header). It also verifies the mock was used correctly (assert_called_once_with) confirming that the Use Case called the dependency with the right ID.
