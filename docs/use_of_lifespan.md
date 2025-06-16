### [<- back](_index.md)

#### Project - Insert project title
# Use of Lifespan

Explanation and clarifications on the use of lifespan.

<br>

## Document Contents

This document contains:

- **What is Lifespan?**
- **What is it For?**
- **When Should You Use It?**
- **Does It Work for Any Service (Detail) Like a DB, Messaging, etc.?**
- **What Criteria Should I Use to Determine Whether to Use Lifespan?**
- **How Do I Define It in the Lifespan File If I Have More Than One Service?**

<br>

# What is Lifespan?

`lifespan` is a feature of `ASGI applications` (like FastAPI and Starlette) that allows you to define code executed at key moments in the application's lifecycle:

1. `Once at startup`: Before the application starts receiving and processing HTTP requests.
2. `Once at shutdown`: After the application has stopped processing HTTP requests and is about to shut down.

It's typically implemented using an asynchronous context manager (`@contextlib.asynccontextmanager`) in Python, with a function containing a `yield`. The code before the yield is the "startup" phase, and the code after the yield is the "shutdown" phase.

<br>

# What is it For?

Its primary purpose is managing shared resources that are needed for the entire duration of your application's life. It allows you to:

- `Initialize costly resources`: Create database connections, connection pools, persistent HTTP client instances, load large models or configurations, etc., just once at startup.

- `Share resources`: Place the initialized instances of these resources in an accessible location (like app.state) so dependencies can inject them.

- `Gracefully clean up resources`: Ensure connections are closed, temporary files are cleaned up, clients are disconnected, etc., when the application shuts down, preventing resource leaks.

<br>

# When Should You Use It?

You should use `lifespan` whenever your application needs a resource that meets one or more of these criteria:

- It requires `connections` that should be reused across requests (e.g., database, Redis, message queue).
- It's `costly` or `slow to initialize` (e.g., loading a large model, establishing multiple initial connections).
- It requires explicit `cleanup` or `closing` when the application process stops (e.g., closing connection pools, disconnecting network clients).
- It needs to maintain `state` that is relevant for multiple requests or components (e.g., an application-level in-memory cache).
It has an `Application Scope` rather than just a Request Scope – the instance should live for the entire application's lifetime.

<br>

# Does It Work for Any Service (Detail) Like a DB, Messaging, etc.?

`Yes, absolutely`. lifespan is precisely the tool designed to manage the instances of your infrastructure implementations (the "details") that require a lifecycle. It's ideal for:

- `Database connection` pools (SQL, NoSQL).
- `Messaging system` clients (Kafka, RabbitMQ).
- `Caching` clients (Redis, Memcached).
- Persistent HTTP clients for `calling other external APIs` (httpx.AsyncClient is a prime example).
- Loading configurations or models that are used throughout the app.

<br>

# How Do I Define It in the Lifespan File If I Have More Than One Service?

If you have multiple resources that need `lifespan` management, you initialize and clean up `all of them within the same single lifespan function` that you pass to the FastAPI() constructor.

- Before the yield `(Startup)`: Initialize each resource one by one. Assign each initialized instance to a unique key in `app.state.`

```python

# Conceptual example of startup with multiple resources
app.state.database_pool = await initialize_database_pool(...)
app.state.http_client = httpx.AsyncClient(...)
app.state.message_queue_producer = await connect_to_message_queue(...)
# ... initialize other resources ...

```

- After the yield `(Shutdown)`: Retrieve each instance from `app.state` and call its asynchronous close method `(close(), aclose(), disconnect(), shutdown(), etc.)` one by one. It's good practice to close them in reverse order of opening if there are dependencies.

```python

# Conceptual example of shutdown with multiple resources
# Close resources in reverse order if needed
if hasattr(app.state, 'message_queue_producer') and app.state.message_queue_producer:
    await app.state.message_queue_producer.close()

if hasattr(app.state, 'http_client') and app.state.http_client:
    await app.state.http_client.aclose() # Use .aclose() for httpx.AsyncClient

if hasattr(app.state, 'database_pool') and app.state.database_pool:
    await app.state.database_pool.close()

# ... close other resources ...

```

You can use helper functions (within the same lifespan.py file or in separate modules) to encapsulate the detailed initialization and cleanup logic for each resource, keeping the main lifespan function cleaner as a high-level orchestrator.