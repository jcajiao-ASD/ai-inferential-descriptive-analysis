### [<- back](_index.md)

#### Project - Insert project title
# Project fundamentals

Explanation of the architecture, practices and fundamentals of the project.

<br>

## Document Contents

This document contains:

- **Context of the Project**
- **Quick summary of the layers**
- **Clean Architecture**
- **REST API**
- **Conclusion**

<br>

# Context of the Project
The project is built under a domain-centric architecture [[INFO]](https://dev.to/dazevedo/domain-centric-architecture-building-software-that-aligns-with-business-needs-48n5) following Robert C. Marting's Clean Architecture practices.

For the construction of the APIs we follow the REST (Representational State Transfer) architectural style [[INFO]](https://www.geeksforgeeks.org/rest-api-architectural-constraints/), defined by Roy Fielding.

In search of software quality assurance, priority is given to the creation of unit tests [[INFO]](https://medium.com/simform-engineering/importance-of-unit-testing-in-software-development-3f47ef326be1), which allow validating the software behavior.

<br>

# Quick summary of the layers

```bash
.
├── application
│   ├── interface
│   ├── mappers
│   └── use_case
│       └── pokemon
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
- core: General configuration, startup/shutdown (lifespan) and “glue” of the application..

<br>

# Clean Architecture

Clean Architecture is a software design proposed by Robert C. Martin in his book “Clean Architecture: A Craftsman's Guide to Software Structure and Design”, creating a philosophy and a set of principles for organizing the code of an application.

The goal is to create systems that are:

- Frameworks Independent: You can change your web framework or UI without rewriting your business logic.
- Testable: The business logic can be tested without the UI, database, web server, etc.
- UI Independent: You can change the UI without changing the business logic.
- Database Independent: You can change your database without changing your business logic.
- External Agent Independent: Your business logic is not tied to external APIs or other services.

To achieve this independence, the Clean Architecture organizes the code in concentric layers (like the rings of an onion or a target). The fundamental rule of this architecture is the Dependency Rule:

- Code dependencies can only point inward.
- Inner layers cannot know anything about outer layers.

In short, Clean Architecture is an architectural style that helps to organize code in layers based on the “Dependency Rule” (always inward) to keep your core business logic (Domain and Use Cases) independent of external technical details, making the software easier to test, maintain and evolve.

**Study resources**
- [Clean Architecture: Simplified and In-Depth Guide](https://medium.com/@DrunknCode/clean-architecture-simplified-and-in-depth-guide-026333c54454)

- [Complete Guide to Clean Architecture](https://www.geeksforgeeks.org/complete-guide-to-clean-architecture/)

- [Introducción a las “Clean Architectures”](https://medium.com/@diego.coder/introducci%C3%B3n-a-las-clean-architectures-723fe9fe17fa)

- [Arquitectura Limpia (Chapter-by-chapter explanation of the book Arquitecture Limpia) - YouTube](https://youtube.com/playlist?list=PL0kIvpOlieSOsp6zCdo5QiX3uMIZT5dNu&si=6zyGoGiNTmVRuuyr)

- [Arquitectura Limpia by Fernando Herrera - YouTube](https://youtube.com/watch?v=zCBU_kkaeyY&si=1lWM9lVa85egeFsz)

<br>

# REST API

In essence, REST is not a standard or a specific technology, but an architectural style for designing distributed systems (such as web applications) that focuses on stateless communication between a client and a server. It was defined by Roy Fielding in his doctoral dissertation.

The main goal of REST is to make web systems:

- Scalable: Easy to expand to handle more users and data.
- Reliable: Less prone to failure.
- Modifiable: Easy to change and evolve over time.
- Visible: Easy to monitor and understand.
- Portable: Easy to move or reuse in different environments.
- Simple: Easy to understand and build.

<br>

To achieve this, a system that adheres to the REST architecture must comply with a number of architectural constraints (principles):

- Client-Server: the client (e.g. browser, mobile app) is separate from the server (where the logic and data reside). This allows them to evolve independently.

<br>

- Stateless: Each request from the client to the server must contain all the information the server needs to understand and process it. The server does not store information about the client's session or state between requests.

<br>

- Cacheable: Server responses can indicate whether information can be cached by the client or by intermediate components to improve performance.

<br>

- Layered System: Communication between client and server can pass through intermediate layers (proxies, gateways, firewalls) without the client or the end server necessarily knowing, that favors scalability and security.

<br>

- Uniform Interface: This is the central and most important constraint. It means that the way the client interacts with the server is always the same, regardless of the specific resource. This is achieved through several sub-restrictions:

  - Resource Identification: Each “thing” or piece of data (a resource) is uniquely identified by a URI (e.g., a URL such as /users/123).

  - Self-describing messages: Each message (request or response) contains enough information (using standard HTTP methods, headers, media types such as application/json) for the receiver to understand how to process it.

  - Hypermedia as the Application State Engine (HATEOAS): Representations of resources must include links to other related resources or available actions. The client navigates the API by following these links rather than having the URIs rigidly pre-coded. (This constraint is often the least implemented in “real world” APIs).

<br>

- Code-On-Demand (Code-On-Demand - Optional): The server can extend client functionality by sending executable code (e.g. JavaScript for a web page). It is optional and less common in pure REST APIs that do not serve web pages.


<br>

**Study resources**
- [REST API Introduction](https://www.geeksforgeeks.org/rest-api-introduction/)
- [Best practices for REST API design](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/)

<br>

# Conclusion

Using the architectural patterns of Clean Architecture and REST to create fastAPI backend systems that are easy to maintain and scale, secure to use and reliable, combating technical debt, spaghetti code and improving the flexibility of the development experience.