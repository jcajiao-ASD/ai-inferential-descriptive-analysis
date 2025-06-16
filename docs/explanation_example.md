### [<- back](_index.md)

#### Project - Insert project title
# Explanation of the example

This document explains how the scaffold is structured and how a simple code example demonstrates the application of its architectural principles in practice.

<br>

## Document Contents

This document contains:

- Context of the example
- Quick summary of the layers
- The Example Structure (Dependency Order)

***

<br>

# Context of the example

The scaffold was built with a clean and minimal base, **providing the Domain, Application, Infrastructure, Presentation, and Core layers.** This structure helps create maintainable, scalable, and testable applications by managing dependencies and separating concerns.

The example created for this scaffold illustrates these principles by showing how to fetch data from an external API (the PokeAPI, which provides information about Pokémon) using the structured layers.

<br>

# Quick summary of the layers

Here's a quick look at the main parts of the project structure:

```bash
.
├── application     # The app's specific jobs and actions.
│   │
│   ├── interface   # Lists things the application needs from outside 
│   │               # (like talking to a database), without showing how.
│   │
│   ├── mappers     # Code that changes data format for different parts.
│   │
│   │
│   └── use_case    # The code for every specific job the application does.
│       │
│       └── pokemon # Example folder for Pokemon actions.
│
├── core            # Important setup code and common tools.
│   │
│   │
│   └── lifespan    # Code that runs when the application starts and stops.
│   
├── domain          # Core business ideas and rules (like what a 'Pokemon' is).
│   │
│   │
│   ├── entities    # Defines the main things in the business.
│   │
│   │
│   └── exceptions  # Defines specific error messages for business problems.
│
│   
├── infrastructure  # Code that knows how to talk to outside things (databases, APIs).
│   │
│   │
│   ├── service     # Specific code for talking to different outside services.
│   │
│   │
│   └── shared      # Helper code for connecting to external things.
│   
│   
└── presentation  # Handles requests from the outside (like web calls) and sends responses back.
    │   
    │   
    ├── api         # The code for the web API addresses.
    │   │
    │   │
    │   ├── healthcheck # The address to check if the app is healthy.
    │   │
    │   │
    │   └── v1      # Folder for version 1 addresses.
    │
    │   
    ├── middleware  # Code that runs before or after handling a request.
    │
    │   
    └── utils       # Helper code for handling requests.
       
```
<br>

- domain: The independent heart; pure business rules and core concepts (Entities, Exceptions).
- application: The app-specific actions (use cases); defines interfaces (ports) needed from external services.
- infrastructure: The external details (DBs, external APIs); implements the interfaces defined in Application.
- presentation: Handles the external interface (your REST API); receives requests and calls Application.
- core: Configuration and setup; manages application startup/shutdown (lifespan) and wires dependencies.

<br><br>

# The Example Structure (Dependency Order)
Let's explore the components of the example, starting from the core independent layer and moving outwards, showing how each part depends on those inside it or defines contracts for those outside.

<br>

1. The Core Concepts: Domain (Entity and Exception)

These are the innermost pieces, representing the fundamental business concepts and any errors specific to those concepts. They are the most independent part of your application and are used by the layers around them.

```python

# src/domain/entities/pokemon.py (Entity)

@dataclass
class Pokemon:
    id: int
    name: str
    types: List[str] = field(default_factory=list)


# src/domain/exceptions/pokemon.py (Exception)

class PokemonNotFoundError(Exception):
    def __init__(self, identifier: str | int):
        self.identifier = identifier
        super().__init__(f"Pokemon with identifier '{identifier}' not found.")

``` 
(The Application and Infrastructure layers will use these Domain concepts.)

<br><br>

2. The Application's Logic Definition: Application (Interface, Mapper, Use Case)

This layer contains the application's specific business rules and orchestrates the flow. It depends only on the Domain layer and defines interfaces (ports) for what it needs from external layers.

```python
# src/application/interface/pokemon_api_client.py (Interface/Port)

class PokemonApiClientInterface(abc.ABC): # <-- Defines the contract
    @abc.abstractmethod
    async def get_pokemon_by_id(self, pokemon_id: int) -> Pokemon:

```
(The Use Case below will depend on this Interface.)

```python
# src/application/mappers/pokemon_mapper.py (Mapper)

class PokemonMapper:
    @staticmethod
    def from_pokeapi_response(data: dict[str, Any]) -> Pokemon:
        types_list: list[str] = []
        if "types" in data and isinstance(data["types"], list):
            for type_info in data["types"]:
                if (
                    isinstance(type_info, dict)
                    and "type" in type_info
                    and isinstance(type_info["type"], dict)
                    and "name" in type_info["type"]
                ):
                    types_list.append(type_info["type"]["name"])

        return Pokemon(id=data.get("id"), name=data.get("name"), types=types_list)

```

(This Mapper is used by the Infrastructure layer implementation when fetching data.)

```python

# src/application/use_case/pokemon/get_pokemon_by_id.py (Use Case)

class GetPokemonByIdUseCase:
    def __init__(self, pokemon_api_client: PokemonApiClientInterface):
        self._pokemon_api_client = pokemon_api_client

    async def execute(self, pokemon_id: int) -> Pokemon:
        pokemon = await self._pokemon_api_client.get_pokemon_by_id(pokemon_id)
        return pokemon

```

(This Use Case will be called by the Presentation layer (Endpoint), and it needs an implementation of PokemonApiClientInterface to be injected.)

<br><br>

3. The External Details: Infrastructure (Service Implementation)

This layer is external and depends on the Application layer's Interfaces. It contains the concrete implementations of how to interact with the outside world (databases, external APIs, etc.) and knows about technical details and external libraries.

```python

# src/infrastructure/service/pokeapi_client.py (Infrastructure Service)

class PokeApiHttpClient(PokemonApiClientInterface): 
    def __init__(self, client: httpx.AsyncClient, base_url: str = "https://pokeapi.co/api/v2"):
        self._client = client 
        self._base_url = base_url
        self._mapper = PokemonMapper() 

    async def get_pokemon_by_id(self, pokemon_id: int) -> Pokemon:
        url = f"{self._base_url}/pokemon/{pokemon_id}"

        try:
            response = await self._client.get(url) 
            response.raise_for_status()
            data = response.json()
            return self._mapper.from_pokeapi_response(data) 

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                 raise PokemonNotFoundError(pokemon_id) from e
            print(f"HTTP error occurred: {e}")
            raise

        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
            raise 

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise 

    async def close(self):
        await self._client.aclose() 

```

(This implementation will be instantiated in the Core layer and injected into the Use Case in the Application layer.)

<br><br>

4. Application Setup and Wiring: Core

The Core layer is outside the concentric circles but is crucial for bootstrapping the application. It knows about all the concrete implementations and wires them together, often managing the lifecycle of shared resources.

```python

# src/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # CORS
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = False
    allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    allow_headers: list[str] = ["*"]

    # POKE API
    poke_api_url: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

```
<br>

```python

# src/core/app_lifespan.py (Lifespan - Core)

@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the application lifecycle: startup and shutdown.

    Initialize and close shared resources such as HTTP clients.
    Resources are stored in app.state.
    """
    httpx_client_instance = httpx.AsyncClient(base_url=settings.poke_api_url)

    app.state.httpx_client = httpx_client_instance

    pokemon_api_client_instance = PokeApiHttpClient(client=httpx_client_instance)

    app.state.pokemon_api_client = pokemon_api_client_instance

    yield

    if hasattr(app.state, "pokemon_api_client") and app.state.pokemon_api_client:
        await app.state.pokemon_api_client.close()

```

(This lifespan function makes the PokeApiHttpClient instance available via app.state for dependency injection.)

<br><br>

5. Defining Dependency Providers (dependencies.py - Presentation/API)

This file, part of the Presentation layer (specifically within the API package), defines functions that tell FastAPI's Depends system how to retrieve or create the instances needed by endpoints. These providers access the resources set up in the Core/Lifespan layer.


```python
# src/presentation/api/v1/dependencies.py (Dependency Providers)

def get_pokemon_api_client(request: Request) -> PokeApiHttpClient:
    return request.app.state.pokemon_api_client


def get_pokemon_by_id_use_case(
    pokemon_client: PokeApiHttpClient = Depends(get_pokemon_api_client), # <-- Use Case dependency provided here
) -> GetPokemonByIdUseCase:
    return GetPokemonByIdUseCase(pokemon_api_client=pokemon_client)


```

<br><br>

(These provider functions are used by the Endpoint in the Presentation layer to get instances for its parameters.)


6. Handling External Requests: Presentation (Endpoint, Middleware)

The Presentation layer is the outermost layer that interacts with the outside world. The API endpoint receives incoming requests, and middleware handles concerns like CORS before/after the request reaches the endpoint.

```python

# src/presentation/api/v1/pokemon/pokemon_controller.py (Endpoint - Presentation)

router = APIRouter() 

@router.get(
    "/{pokemon_id}", 
    response_model=Pokemon, 
    summary="Get a Pokémon by ID",
    description="Retrieve a specific Pokémon's data by its ID.",
)
async def get_pokemon_by_id_endpoint(
    pokemon_id: Annotated[int, Path(..., gt=0)], 
    use_case: Annotated[GetPokemonByIdUseCase, Depends(get_pokemon_by_id_use_case)], 
    response: Response, 
):
    try:
        pokemon = await use_case.execute(pokemon_id=pokemon_id)
        response.headers["Cache-Control"] = "public, max-age=3600"
        return pokemon

    except PokemonNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Pokemon with ID {pokemon_id} not found."
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred.",
        ) from e

# src/presentation/middleware/cors.py (Middleware - Presentation)

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=settings.allow_credentials,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
    )

```

(These components handle the web interface and use dependencies provided by inner layers.)

7. The Application Mount Point: main.py.

This is the application's entry point. It assembles the top-level components: creates the FastAPI app, attaches the lifespan (which sets up resources in Core), adds middleware (Presentation), and includes the routers (Presentation) that contain the endpoints.

```python
# main.py (Application Entry Point)

app = FastAPI(
    title="Domain services - Project",
    description="Description services",
    version="0.0.1",
    contact={
        "name": "Grupo ASD S.A.S",
        "url": "https://www.grupoasd.com/contacto/",
    },
    lifespan=app_lifespan, # This triggers resource setup/cleanup
)

add_cors_middleware(app) # Add middleware

app.include_router(healthcheck_router.router, tags=["healthcheck"], prefix="/api")
app.include_router(pokemon_controller.router, tags=["pokemon"], prefix="/api/v1/pokemon") # <-- Router from Presentation included here

```