📦 Mercury Order Platform (Learning Project)

A minimal event-driven distributed system built to understand:

API → Queue → Worker architecture
Docker container isolation
Redis-based message passing
Basic async job processing

⚠️ This is a learning implementation.
DB is in-memory and not production safe yet.

🧠 Architecture
Client
  ↓
FastAPI (API Service)
  ↓ (push job)
Redis (Queue / Broker)
  ↓ (consume job)
Worker Service
  ↓
In-memory DB (temporary)
⚙️ Tech Stack
Python 3.11
FastAPI
Redis (message broker)
Docker + Docker Compose
Uvicorn
🚀 How to Run
1. Start everything

From project root:

docker compose up --build

This will start:

API service → http://localhost:8000
Worker service → background consumer
Redis → message broker
🧪 API Endpoints
Health check
curl http://localhost:8000/healthz

Response:

{"status": "ok"}
Create order
curl -X POST http://localhost:8000/orders \
-H "Content-Type: application/json" \
-d '{
  "item": "laptop",
  "quantity": 1
}'

Response:

{
  "order_id": "uuid",
  "status": "queued"
}
Get order status
curl http://localhost:8000/orders/{order_id}

Example:

{
  "status": "completed",
  "item": "laptop",
  "quantity": 1
}
👷 Worker Behavior

The worker:

Continuously listens to Redis queue
Fetches jobs using BRPOP
Processes order
Updates in-memory DB

Logs:

[WORKER] started
[WORKER] processing <order_id>
[WORKER] completed <order_id>
🔍 Debugging
View API logs
docker logs -f <api_container_id>
View Worker logs
docker logs -f <worker_container_id>
Check running containers
docker ps
🧠 Key Learning Concepts
1. Process Isolation

Each container has its own memory → no shared Python state.

2. Queue Decoupling

API does not wait for worker → uses Redis queue.

3. Event-driven flow

API produces events, worker consumes them asynchronously.

⚠️ Current Limitations

This system is intentionally simplified:

❌ No persistent database (in-memory only)
❌ No retry mechanism
❌ No dead-letter queue
❌ No idempotency handling
❌ No failure recovery
🔥 Next Improvements (Roadmap)
Add PostgreSQL (source of truth)
Add retry + failure handling
Add idempotency layer
Add monitoring/logging (Prometheus)
Replace in-memory DB completely
Add Kubernetes deployment
🧠 Why this project exists

To understand:

“Why distributed systems require queues, databases, and isolation”

Not just to build APIs—but to understand system behavior under failure.

🚀 Run Order Summary
docker compose up --build

Then:

Send POST /orders
Watch worker logs
Fetch order status
Observe async processing