✍️ System Understanding (Day 1 – Order Processing System)

API is the front layer of the system where all client requests are received.

The API performs three main responsibilities:

It writes the order state into the database (e.g., status = queued/created)
It pushes a job message into the queue for asynchronous processing
It reads order state from the database when requested

In this implementation, both the database and queue are simulated using in-memory data structures (dictionary for DB and list for queue). This is only for learning purposes. In real production systems, the database is persistent storage (e.g., PostgreSQL) and the queue is a managed messaging system (e.g., AWS SQS or Redis Streams).

The queue is not accessed or processed by the API. It only receives jobs from the API. The worker service is responsible for consuming messages from the queue, processing them, and updating the database accordingly (e.g., changing status from queued → processing → completed/failed).

The /debug/queue endpoint is used only for development visibility. It directly exposes the current in-memory queue state to help understand how jobs are being processed.

Since both the database and queue are in-memory in this setup, the system has a single point of failure: if the process restarts, all data is lost. This limitation is intentional for learning purposes and will be replaced later with persistent storage and managed services.