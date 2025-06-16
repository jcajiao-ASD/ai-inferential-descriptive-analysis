### [<- back](_index.md)

#### Project - Insert project title
# Initialize Project

Welcome to the repository initialization documentation. This document describes the process for starting the
project locally, detailing the necessary steps and providing relevant information about the content of this file.

## Document Contents

This document includes:

- **Prerequisites:** List of tools, versions and dependencies needed.
- **Installation and Configuration:** Step-by-step guide to clone, install dependencies, configure environment
variables and run the project.
- **Additional Notes:** Tips, solutions to common problems and links to external documentation.

## Prerequisites:
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
  pip install "fastapi[standard]" 'uvicorn[standard]' ruff pytest -U pytest-asyncio
  ```

- Run the project:
  ```bash
  uvicorn main:app --port 8000 --reload
  ```
- Open the browser and enter http://127.0.0.1:8000