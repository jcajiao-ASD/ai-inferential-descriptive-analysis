### [<- back](_index.md)

#### Project - Insert project title
# IDE Configuration

The following document contains the configuration of vs code (v. 1.99.3)
and pycharm version (2025.1). For other IDES a solution for importing the
defined rules will be given. This documentation is created as of May 5, 2025.

## Document Contents

This document includes:
- **Configuration rules**: Setting Up Your Development Environment for Ruff
- **Configuration vs code**: Explanation of how to set up vs code rules
- **Configuration of jetbrains products for pycharm**: Explanation of how to set up jetbains products for pycharm
- **Solution for other IDES**: Explanation of how to import rules for other IDEs

# Configuration rules:
To make coding easier and ensure your code follows the project's style
and quality rules automatically, we use a tool called Ruff.
Ruff acts as both a code linter (finding potential issues and style problems)
and a formatter (automatically fixing style problems).

The project's specific rules for Ruff are defined in the ruff.toml file at the
root of the project. Your IDE (like VS Code, PyCharm, etc.) can read this file
and help you code according to these rules in real-time.

## Here’s how to get started:

1. Install the Ruff Extension/Plugin:
The first step is to install the official Ruff extension or plugin
available for your specific IDE. Search for "Ruff" in your IDE's
extensions or plugins marketplace and install it. This is what
connects your IDE to the Ruff tool.

- [Ruff Extension for Vs Code](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- Pycharm does not have an official extension, but the company ASTRAL, creator of RUFF, offers a solution for this.

## Understand Key Style Settings (and check your IDE):

Ruff will handle most formatting automatically, but it's good to be aware
of the main style choices defined in ruff.toml:

- Line Length: Code lines should not be longer than 100 characters 
- Indentation: We use 4 spaces for indentation (indent-width = 4, indent-style = "space").
- Quotes: We use double quotes (") for strings (quote-style = "double").

## Why is this helpful?

Integrating Ruff with your IDE is like having an automated coding assistant:

- It gives you instant feedback on potential problems and style violations.
- It automatically fixes many style issues for you.
- It ensures that the code you write matches the project's standards without you 
  having to manually remember every rule.
- Setting up the Ruff plugin in your IDE is highly recommended for a smooth and
  productive development workflow that aligns with the project's code quality goals.


# Configuration vs code
From ADC (Architecture, Design and Construction) we seek to provide the ideal
configuration for the progress of the project, so the configuration of vs code
will be in a GitHub Gist for configuration of the tool. -> [Gist](https://gist.github.com/jcajiao-ASD/652a6fc723ec6147f1ed6b60558071d3) 

1. Create the .vscode folder in the root of the project
2. Create the settings.json file inside the .vscode folder
3. Copy the content of the [Vs Code Gist](https://gist.github.com/jcajiao-ASD/652a6fc723ec6147f1ed6b60558071d3) and paste into settings.json


# Configuration of jetbrains products for pycharm
From ADC (Architecture, Design and Construction) we seek to provide the ideal
configuration for the progress of the project, so the configuration of pycharm
will be in a GitHub Gist for configuration of the tool. -> [Pycharm Gist]() 

1. Create the .idea folder in the root of the project
2. Create the Project.xml file inside the .idea folder
3. Copy the content of the [Pycharm Gist](https://gist.github.com/jcajiao-ASD/e441a250dcfa1161c4be0f32f0221ad0) and paste into Project.xml
4. In the following link is the explanation of how to finish the RUFF integration in pychar (RUFF official documentation) -> [Link](https://docs.astral.sh/ruff/editors/setup/#pycharm)

# Solution for other IDES

Some development tools provide the facility to import rules from one tool to another,
but the configurations that have been created are at the project level, not global,
so importing rules is not possible.

To combat this problem you should consult the official documentation [Link](https://docs.astral.sh/ruff/editors/setup/), 
which explains step by step how to solve this problem.

To have the basic definition of the rules you can run the following pront created
for OpenAI, Gemini or Antropic AI models to get guidance on how to perform the basic
configuration of the following rules in the development tool

```

  You are an expert assistant in configuring development environments and code tools. I need your help to configure some basic code style rules in my development tool.

  Context:
  I am working on a programming project and want to ensure my development environment is configured to follow the code style rules defined for the project. This helps me maintain consistency and avoid common formatting errors.

  Problem/Objective:
  I need step-by-step instructions or the necessary configuration to apply the following basic code style rules in my specific development tool.

  Specific Configuration Rules:
  Here are the basic code style rules I need to configure:
  1.  Line Length: Code lines should not be longer than 100 characters.
  2.  Indentation: We use 4 spaces for indentation.
  3.  Quotes: We use double quotes (") for strings.

  Constraints/Notes:
  -   My development tool is: [INSERT THE NAME AND VERSION OF YOUR DEVELOPMENT TOOL HERE]
  -   My programming language is: Python
  -   The explanation should be: I want a [SIMPLE / TECHNICAL / STEP-BY-STEP - CHOOSE ONE OR COMBINE]

  Desired Result:
  Clear instructions or code snippets (like JSON, XML, configuration commands) explaining how to set the specified Line Length, Indentation, and Quotes rules within my development tool.
  

```