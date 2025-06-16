### [<- back](_index.md)

#### Project - Insert project title
# Testing

This document describes the tools, commands and configurations performed for the execution of the tests.

## Document Content

This document includes:

- **Libraries**: Libraries used in the project.
- **Configurations**: Configurations used in the project.
- **Commands**: Tools and commands used in the project.

### Libraries

- Pytest 8.3.4

### Configurations

- **Pytest**: The pytest.ini file contains the settings for the execution of the tests, defining file paths, test naming convention and the project directory path.

The current configuration is as follows:
```
[pytest]
python_files = tests/*.py # Definition of the test files to be executed
pythonpath = . # Sets the project root directory, allowing imports to work correctly
```

### Commands

- To run the tests (Must be performed in the root of the project)

```shell
pytest
```

- To obtain the test report in HTML format to be consulted on the web, perform the following command
```shell
pytest --cov=src --cov-report=html
```

- To obtain the test report in XML, perform the following command
```shell
pytest --cov=src --cov-report=xml
```