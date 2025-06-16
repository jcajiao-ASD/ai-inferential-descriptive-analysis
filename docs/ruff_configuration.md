### [<- back](_index.md)

#### Project - Insert project title
# RUFF Configuration

This document describes the configuration set up of the RUFF tool.

## Document Contents

This document includes:
- **What is RUFF?:** Description of what RUFF is and the purpose of RUFF.
- **Actual Configuration:** Explanation of RUFF's current configuration for following conventions and best practices.

### What is RUFF?
An extremely fast Python linter and code formatter, written in Rust. Linting the CPython codebase from scratch. Ruff aims to be orders of magnitude faster than alternative tools while integrating more functionality behind a single, common interface. [Reference](https://docs.astral.sh/ruff/)

### Actual Configuration

Here we present the current RUFF configuration used in the project. This configuration is defined in the `ruff.toml` file at the root of the project. Understanding it will help you write code that adheres to the quality and style standards we follow.

```toml
### Actual Configuration

Here we present the current RUFF configuration used in the project. This configuration is defined in the `ruff.toml` file at the root of the project. Understanding it will help you write code that adheres to the quality and style standards we follow.

```toml
line-length = 100
indent-width = 4


target-version = "py312"


src =       [   
                "src/"
            ]


exclude =   [
                "docs/*",
                "venv/*",
            ]


include =   [
                "main.py"
            ]


[format]
docstring-code-format = true
docstring-code-line-length = 80
skip-magic-trailing-comma = false
indent-style = "space"
line-ending = "lf"
quote-style = "double"



[lint]
select =    [
                "E", # pycodestyle errors
                "F", # Pyflakes errors
                "I", # Import sorting (isort)
                "D", # Docstring rules
                "N", # Naming conventions (PEP 8)
                "UP", # Modernize code (pyupgrade)
                "B", # Possible errors (bugbear)
                "RUF", # Ruff-specific rules
                "PIE", # More Pythonic code (flake8-pie)
                "ARG", # Unused arguments (flake8-unused-arguments)
                "TCH", # Type checking conventions (flake8-type-checking)
                "ASYNC", # Rules for asyncio (flake8-async),
                "FAST" # FastAPI rules (FAST)
            ]


ignore =    [
                "D212",  # Ignore "multi-line-summary-first-line" (preferring D213)
                "D211",  # Ignore "no-blank-line-before-class" (preferring D203)
                "D203",  # Ignore "one-blank-line-after-class-definition" (conflict with formatter)
            ]


[lint.per-file-ignores]
"__init__.py" = ["D104"]
"src/presentation/api/**/*.py" = ["B008"]

```

Let's break down each part of this configuration:

General Configuration:

- line-length = 100: Defines the maximum allowed length for a line of code as 100 characters. This helps keep code readable without lines becoming excessively long.

- indent-width = 4: Sets the indentation to be 4 spaces. This is a common convention in Python (PEP 8).

- target-version = "py312": Informs RUFF that the code is written for Python 3.12. This is important for RUFF to apply rules and optimizations compatible with this specific language version.

- src = ["src/"]: Specifies that the project's primary source code is located inside the src/ directory. RUFF will focus its checks on files within this path.

- exclude = ["docs/*", "venv/*"]: Tells RUFF to ignore specific directories and their contents, such as the documentation output (docs/*) and the virtual environment (venv/*). We don't need to lint or format code within these folders.

- include = ["main.py"]: Specifies specific files that should be included in the checks, even if they are not directly within the src path. In this case, it ensures the main.py file at the project root is checked.

[format] Section:

This section controls how RUFF will automatically format the code.

- docstring-code-format = true: Enables formatting for code blocks found within docstrings.

- docstring-code-line-length = 80: Sets a specific line length of 80 characters for code blocks inside docstrings, potentially different from the general line-length.

- skip-magic-trailing-comma = false: Controls whether Ruff should add a trailing comma for tuple singletons (e.g., (1,)). Setting it to false means Ruff will handle this according to its standard formatting rules.

- indent-style = "space": Confirms that indentation will be done using spaces (instead of tabs), aligning with the general indent-width setting.

- line-ending = "lf": Ensures that line endings in the files are "lf" (line feed), which is the standard on Unix-like systems and is preferred for version control like Git.

- quote-style = "double": Indicates that double quotes (") should be used for strings. While single quotes (') are also valid in Python, using a consistent style improves readability.

[lint] Section:

Here we define which linting rules RUFF will apply.

- select: This list contains the codes for the rule sets we want to enable. Each code represents a linter or a set of checks. The selected rule sets cover common issues like formatting, potential errors, import sorting, naming conventions, code modernization, docstring style, and specific rules for Ruff, Pythonic code, unused arguments, type checking, asyncio, and FastAPI.

- ignore: This list specifies rules that are explicitly disabled.

    - "D212": Ignores the rule requiring the first line of a multi-line docstring to be on a new line. This is often ignored in favor of D213, which allows the summary on the first line.

    - "D211": Ignores the rule that checks for a blank line before a class definition line. This is ignored to prefer the style enforced by the Ruff formatter.

    - "D203": Ignores the rule that requires one blank line between the class definition line and the first line of its docstring. This rule conflicts with the opinionated style enforced by the Ruff formatter, so it is ignored to avoid conflicts.

[lint.per-file-ignores] Section:

This section allows ignoring specific rules only for certain files or patterns.

- "__init__.py" = ["D104"]: This ignores the D104 rule (missing docstring in __init__ file) specifically for all __init__.py files in the project. It's common to skip docstrings for simple __init__.py files that just handle imports.

- "src/presentation/api/**/*.py" = ["B008"]: This ignores the B008 rule (Do not perform function call in argument defaults) for all Python files within the src/presentation/api/ directory and its subdirectories. This is commonly done in FastAPI projects to avoid warnings on parameters using Depends(...), Path(...), Query(...), etc., as these are standard practices with FastAPI's dependency injection and parameter validation, despite Ruff's general warning against function calls in defaults.

***Importance of this Configuration:***

Using RUFF with this configuration allows us to maintain a clean, consistent, and bug-free codebase from the early stages of development. By automating style checks and potential issue detection, we can focus more on the business logic of our API, built with FastAPI, knowing that the underlying code adheres to high-quality standards. This facilitates collaboration among developers and reduces the likelihood of introducing style-related bugs or subtle errors.