# System Brain Dump

## Core Flow
User → ALB → API → DB + SQS → Worker → DB + S3

## Components
- API: receives requests
- Worker: processes async jobs
- DB: stores state
- Queue: decouples processing
- Redis: caching/idempotency
- S3: artifacts

## Why queue?
- API stays fast
- retry possible
- failure isolated

## Why DB?
- source of truth
- order lifecycle tracking

## Why Redis?
- fast temporary storage
- avoid duplicate processing

## Failure Thinking
- API can fail → retry client
- Worker fails → message reprocessed
- DB fails → system degraded