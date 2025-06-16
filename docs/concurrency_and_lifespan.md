### [<- back](_index.md)

#### Project - Insert project title
# Concurrency And Lifespan

The following document seeks to explain the possible problems related to concurrency in applications.

<br>

## Document Contents

This document contains:

- **What is concurrency?**
- **What role does lifespan play?**
- **What role do external applications play?**
- **How does FastAPI help avoid concurrency problems?**

<br>

# What is concurrency?
`Think of concurrency as juggling multiple tasks at seemingly the same time`. In software, it's about designing a system that can handle many things happening or being requested around the same moment.

For a web application, concurrency means being able to handle multiple user requests that arrive at the server almost simultaneously. Instead of finishing one request completely before starting the next, a concurrent system can switch between different requests, making progress on several at once.

It's different from parallelism, which is when multiple tasks are actually running at the exact same instant on multiple computer processors. Concurrency is about managing many tasks, while parallelism is about executing many tasks simultaneously.

A big challenge in concurrency, especially for web apps, is waiting. Your app often has to wait for things like a database query to finish, another API to respond, or a file to be read. This waiting time is called I/O-bound work. If your app is stuck waiting on one task, it can't work on others, slowing everything down.

<br><br>

# What role does lifespan play?
In web frameworks like FastAPI, `lifespan` is a feature that lets you run code right when your application `starts up` and again right when it `shuts down`. It's defined using a pattern that creates a temporary `"context"` for your application's life.

The main role of lifespan in concurrency is managing shared resources. Applications often need resources that are used by many different requests throughout the app's life, such as:

- Database connection pools (to efficiently manage database connections)
- Clients for talking to other services (like a persistent HTTP client)
- Caches or message queue connections

These resources are expensive to set up or close for every single request. lifespan solves this by letting you:

1. Initialize these shared resources once when the app starts (before the first request arrives).
2. Store them in a place accessible to your application code (like app.state).
3. Ensure these resources are gracefully closed or cleaned up once when the app stops (after the last request is handled).

So, while lifespan itself doesn't solve concurrency problems within a resource (like preventing two requests from corrupting data in a database – that's the database's job), it provides the essential mechanism to safely and efficiently provide the instances of the shared resources to the potentially thousands of concurrent tasks that will need them during the app's runtime. It prevents overhead and resource leaks under concurrent load by managing the shared resources' lifecycle correctly.

<br><br>

# What role do external applications play?
`"External applications"` or `"external services"` are the other systems your application talks to. This includes:

- Databases
- Other APIs over the internet
- Message queues (like Kafka, RabbitMQ)
- File storage systems
- Caching servers (like Redis)

Interacting with these external systems is typically where I/O-bound waits happen. Your application sends a request (e.g., a database query) and has to wait for the external application to process it and send back a response.

In a concurrent system, many requests from your application will be waiting on these external services simultaneously. Your web application's ability to handle these concurrent waits efficiently is crucial for its overall performance under load.

However, a key factor in concurrency is the performance and capacity limits of the external application itself. Even if your web application is super efficient at waiting, the external service can become a bottleneck.

- If your database can only handle 100 simultaneous queries efficiently, your web app might have 1000 concurrent requests all waiting for one of those 100 database slots. The bottleneck isn't your web app waiting, but the database's processing limit.

- f an external API has strict rate limits (e.g., 10 requests per second), your application can only process features that rely on that API at that limited rate, regardless of how fast your app can make the requests concurrently.

Concurrency problems (like race conditions leading to incorrect data) most often happen at the boundary with these external applications, especially databases, when multiple concurrent tasks try to modify the same data simultaneously without proper synchronization or transaction handling within the external service itself.

# How does FastAPI help avoid concurrency problems?

FastAPI, running on ASGI servers like Uvicorn, primarily helps you manage concurrency efficiently for I/O-bound tasks, rather than automatically solving all possible concurrency problems (like race conditions on shared mutable state).

Here's how it helps:

- Efficient I/O Handling: FastAPI is built on asyncio and the ASGI standard. This allows it to handle a large number of `concurrent requests that involve waiting (I/O)` using a single thread or a small pool of `asynchronous workers`. When your code hits an await (like waiting for a database result or an API response), it releases control, allowing FastAPI/Uvicorn to work on other waiting requests. This is much more efficient than traditional models where a whole thread/process would be blocked just waiting.

- Facilitating Concurrent Code: The `async/await` syntax makes it relatively straightforward to write concurrent code in Python compared to traditional threading models for I/O-bound tasks.

- Structured Resource Management: While not part of the core asyncio model itself, FastAPI's integration of the lifespan concept (using asynccontextmanager) provides a `clean, standard place to manage the lifecycle of those shared resources` (like DB pools, HTTP clients) that are accessed concurrently by many tasks. This helps avoid resource leaks and ensures efficient resource reuse.

- Enabling Concurrent-Safe Dependencies: FastAPI's Dependency Injection system works seamlessly with asynchronous dependencies and resources managed by `lifespan`. This allows your request-handling code to easily access the necessary shared, concurrently managed resources.

It's important to understand that while FastAPI/Uvicorn are great at managing concurrent waits and providing a framework for concurrent I/O, `they do not automatically prevent concurrency problems` like race conditions on shared mutable resources (especially databases or shared in-memory state). Preventing those "clashes" is still the developer's responsibility using tools like:

- Database Transactions and appropriate Isolation Levels.
- Database Atomic Operations (like increment operations).
- Asynchronous Locks (asyncio.Lock) if managing shared mutable state in memory.
- Careful design of interactions with external services based on their concurrency limits.

FastAPI gives you a high-performance asynchronous highway for your requests, making the waiting efficient. It provides tools like lifespan and DI to manage the resources used on that highway. But you still need to build the "intersections" (interactions with shared mutable resources) using concurrency-safe patterns.