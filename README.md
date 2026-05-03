# Mercury Order Platform (Async Processing System)

## Overview

This project demonstrates a **production-style asynchronous processing system** using:

* API service (request ingestion)
* Redis (message queue)
* Worker service (background processing)
* PostgreSQL (source of truth)

The system is designed to handle **component failures without losing data**.

---

## Architecture

```text
Client → API → Redis Queue → Worker → PostgreSQL
```

### Flow

1. Client sends order request to API
2. API:

   * Writes order to PostgreSQL (source of truth)
   * Pushes job to Redis queue (`orders`)
3. Worker:

   * Pulls job from Redis
   * Processes it
   * Updates DB status
4. System remains functional even if worker crashes

---

## Key Concepts Implemented

### 1. Asynchronous Processing

* API does not process jobs directly
* Jobs are delegated to worker via Redis
* Improves scalability and decoupling

---

### 2. At-Least-Once Delivery Guarantee

* Implemented using:

  * `BRPOPLPUSH` (Redis)
  * Separate processing queue (`orders:processing`)

* Jobs are:

  * Moved to processing queue before execution
  * Only removed after successful completion

---

### 3. Failure Handling (Worker Crash Safe)

If worker crashes during processing:

* Job remains in `orders:processing`
* Not lost
* Can be recovered and retried

---

### 4. Stuck Job Recovery

Implemented custom recovery mechanism:

* Each job has `processing_started_at`
* Worker checks processing queue periodically
* If job exceeds timeout:

  * It is requeued back to main queue

```text
processing → timeout → requeue → process again
```

---

### 5. Idempotency Protection (Basic)

Worker checks:

```python
if order.status == "completed":
    skip
```

Prevents duplicate processing in most cases.

---

### 6. Separation of Concerns

* API → handles requests
* Worker → handles processing
* Redis → queue/buffer
* PostgreSQL → source of truth

---

## Tech Stack

* FastAPI
* Redis
* PostgreSQL
* Docker / Docker Compose
* SQLAlchemy

---

## How to Run

### 1. Start services

```bash
docker compose up --build
```

---

### 2. Create order

```bash
curl -X POST localhost:8000/orders \
-H "Content-Type: application/json" \
-d '{"item": "test", "quantity": 1}'
```

---

### 3. Check order status

```bash
curl localhost:8000/orders/<order_id>
```

---

### 4. Inspect queues (optional)

```bash
docker exec -it <redis_container> redis-cli

LRANGE orders 0 -1
LRANGE orders:processing 0 -1
```

---

## Failure Testing

### Simulate worker crash

```bash
docker kill <worker_container>
```

Wait for timeout, then restart:

```bash
docker compose up
```

Expected behavior:

* Stuck job is detected
* Job is requeued
* Worker processes it again

---

## Guarantees Provided

* No job loss
* System continues despite worker failure
* Jobs are eventually processed

---

## Known Limitations (Intentional)

This system is not fully production-grade yet.

Missing:

* Retry limits
* Dead Letter Queue (DLQ)
* Strong idempotency guarantees
* Distributed locking
* Observability (metrics/tracing)

---

## Next Improvements

* Implement retry count + max retry threshold
* Add DLQ (`orders:dlq`)
* Add structured logging + monitoring
* Move to Kubernetes (EKS) deployment
* Replace Redis list with production-grade queue system (SQS / Kafka)

---

## Key Learning Outcomes

This project demonstrates:

* Designing for failure, not just success
* Understanding queue semantics
* Building fault-tolerant async systems
* Handling distributed system edge cases

---

## Summary

This is not a simple CRUD API.

It is a **failure-aware, asynchronous system** that demonstrates:

* Decoupled architecture
* Crash recovery
* Eventual consistency
* Real-world system behavior
