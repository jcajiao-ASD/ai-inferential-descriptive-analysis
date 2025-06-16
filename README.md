# Welcome to the FastAPI scaffold for project construction

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Fast API](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)


## Build with

| Technology |                   Version                   |
|------------|---------------------------------------------|
|  Python    | [3.12.9](https://www.python.org/downloads/) |

<br>

The following is a step-by-step guide for the configuration, initialization and use of the scaffold.


<br><br>

## Step One - Configure your development environment

The scaffold is created to be used with tools like vs code or pycharm, here is a step by step guide to use it:

<br>
<br>

- Visual Studio Code:
    - Install the Ruff extension [LINK](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
    - Install the SonarLint extensión [LINK](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode)
    - In the root of the project create the folder `.vscode`
    - Inside the .vscode directory create the `settings.json` file
    - Copy and paste the following code into `settings.json` file

<br>
<br>

```json

{
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "editor.rulers": [
        100
    ],
    "files.encoding": "utf8",
    "[python].editor.insertSpaces": true,
    "[python].editor.tabSize": 4,
    "[python].editor.defaultFormatter": "ms-python.ruff",
    "editor.formatOnSave": true,
    "python.formatting.provider": "ruff",
    "python.linting.ruffEnabled": true,
    "python.linting.provider": "ruff",
    "python.linting.lintOnSave": true,
    "ruff.linting.enabled": true,
    "ruff.formatting.enabled": true
}


```
<br>
<br>

- Pycharm:
    - Configure the Ruff tool in pycharm [LINK](https://docs.astral.sh/ruff/editors/setup/#pycharm)
    - Install the SonarLint extensión [LINK](https://plugins.jetbrains.com/plugin/7973-sonarqube-for-ide)
    - Create the `.idea` folder in the root of the project
    - Create the `Project.xml` file inside the `.idea` folder
    - Copy and paste the following code into `settings.json` file

<br>
<br>

```xml

<component name="CodeStyleSettingsManager">
  <state>
    <Properties> 
      <option name="TAB_SIZE" value="4" />
    </Properties>
    <Python> 
      <option name="RIGHT_MARGIN" value="100" /> 
      <option name="INDENT_SIZE" value="4" />   
      <option name="TAB_SIZE" value="4" />     
      <option name="USE_DOUBLE_QUOTES" value="true" /> 
      <option name="USE_SINGLE_QUOTES" value="false" />
    </Python>
  </state>
</component>


```

<br>
<br>

## Step Two - Understand the layers of the clean architecture

```
.
├── application
│   ├── interface
│   ├── mappers
│   └── use_case
├── core
│   └── lifespan
├── domain
│   ├── entities
│   └── exceptions
├── infrastructure
│   ├── service
│   └── shared 
└── presentation
    ├── api
    │   ├── healthcheck
    │   └── v1
    ├── middleware
    └── utils

```
Quick summary of the layers:

- domain: The independent heart; business rules and pure entities.
- application: The app-specific actions (use cases); defines interfaces to communicate externally.
- infrastructure: The external details (DB, APIs, etc.); implements the Application interfaces.
- presentation: Handles the external interface (your REST API); calls Application.
- core: General configuration, startup/shutdown (lifespan) and “glue” of the application.

<br>
<br>


## Third step - Copy and paste .env.example

Copy and paste the environment variables from the .env.example file following the steps below.

<br>

- Copy and paste

```bash
cp .env.example .env
```

- Containing `.env`

  - `ALLOW_ORIGINS`: Specifies the list of origins allowed to make CORS requests. In this case, ["*"] means that requests from any domain are allowed.

  - `ALLOW_CREDENTIALS`: Indicates whether credentials (such as cookies or authentication headers) are allowed in CORS requests. A value of False means the server will not allow these credentials.

  - `ALLOW_METHODS`: Lists the HTTP methods permitted for CORS requests. Here, the allowed methods are GET, POST, PUT, and DELETE.

  - `ALLOW_HEADERS`: Defines the headers that can be used during the CORS requests. In this configuration, ["*"] allows any headers.

  - `POKE_API_URL`: Provides the base URL for the external Pokémon API. The value https://pokeapi.co/api/v2 is used to retrieve Pokémon data from that service (`Used for example`).

<br><br>

## Fourth step - Creation of virtual environment and install dependencies

Let's start with the creation of the virtual environment to start the project and look at the example of the scaffold in the following step

<br>

### Prerequisites:
- Python 3.12.x
- pip 25.0.x

<br>

- Create a virtual environment:
  ```bash
  python3.12 -m venv venv
  source venv/bin/activate
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

  <br>

  | Package/Extra       | Main Purpose                                                        | Typically Includes... (Key Dependencies of Extra)                                     |
  | :------------------ | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------ |
  | `fastapi[standard]` | Extra adding standard dependencies for common API features.         | `starlette`, `pydantic`, `httpx` (test client), `email_validator`, `python-multipart` |
  | `uvicorn`           | A very fast ASGI server to run your FastAPI application.            | (Base server)                                                                         |
  | `uvicorn[standard]` | Extra adding dependencies for Uvicorn performance and extra features.| `uvloop`, `httptools`, `websockets`, `watchfiles`, `rich`                             |
  | `ruff`              | An extremely fast linter and formatter for Python code.             | Code analysis, style rule enforcement, automatic formatting.                          |
  | `pytest`            | A popular and extensible framework for writing and running tests.   | Test discovery/execution, assertion tools, fixtures.                                  |
  | `pytest-asyncio`    | Pytest plugin for writing and running asynchronous tests (`async def`).| Handles the asyncio event loop during test execution.                                 |
  | `pytest-cov`        | Pytest plugin to measure test code coverage.                        | Measures and reports on what percentage of your code is covered by tests.             |
  | `pydantic-settings`        | Settings management using Pydantic                        | Features for loading a settings or config class from environment variables or secrets files.             |


<br>

- Run the project:
  ```bash
  uvicorn main:app --port 8000 --reload
  ```
- Open the browser and enter http://127.0.0.1:8000/docs/

<br>
<br>

## Fifth step - Explore the example

An example has been created to explain the functioning of the architecture and the common flow for the creation of a functionality.

<br>

Enter by `clicking` on the following example -> [LINK](docs/explanation_example.md)

<br>
<br>

## Sixth Step - Clean up README.md

Clean up the README.md and configure it based on your project's needs.

<br>
<br>

## Seventh step - Start developing

Inside [docs](docs/_index.md) you will find extra information about `tools, architecture and more`. Remember to feed the `docs` folder with the `features` of your project for easy integration of new developers. `Good luck and Hello World` ç


# Comando de intalación y configuración de Ollama para obtener el wheel de python

CC=/usr/bin/gcc CXX=/usr/bin/g++ CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" pip install --no-cache-dir --force-reinstall --upgrade "llama-cpp-python[server]"