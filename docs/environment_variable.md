### [<- back](_index.md)

#### Project - Insert project title
# Environment Variable

This document details the enviro

## Document Contents

This document includes:
- **Creation of the .env file**: Explanation of the flow to follow for `.env` creation


## Creation of the .env file
You will find an `.env-example` file in the root of the project. This file will be used to contain the body of the environment variables that will contain the `.env` file, from which you will extract the variables for the operation of the project.

1. Defines the environment variables inside the .env-example file.
2. Copy and paste the .env-example file into the root of the project.
3. Change the name of the pasted file to .env

At the end you should have the following structure in your project.

```
.
│ .env
│ .env-example
│  

```
It is important not to delete the .env-example file, for easy initial configuration of the project.

# Note
It is advisable to document the environment variables in this documentation and not in the .env-example file.

## Example of the documentation structure

***Variable title X***
Name:
Description:
How to obtain it?:
Example:
```
DATABASE_MOTOR = "postgresql"
```

