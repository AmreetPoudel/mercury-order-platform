# Mercury Order Platform

A production-style event-driven order processing platform built on AWS using Terraform, EKS, PostgreSQL, SQS, Redis, S3, and GitHub Actions.

## Goal
Demonstrate production-oriented platform engineering across infrastructure as code, Kubernetes operations, CI/CD, observability, resilience, and recovery.

## High-Level Flow
1. Client sends order request to public API endpoint.
2. ALB routes traffic to API service running on EKS.
3. API validates request, stores initial order record in PostgreSQL, and publishes a job to SQS.
4. Worker service consumes the job, processes the order, updates database state, and stores generated artifacts in S3.
5. Monitoring and logging stacks provide visibility into application and infrastructure health.

## Core Technologies
- AWS VPC
- Amazon EKS
- Amazon RDS PostgreSQL Multi-AZ
- Amazon SQS + DLQ
- Amazon ElastiCache Redis
- Amazon S3
- Amazon ECR
- AWS Secrets Manager
- Terraform
- GitHub Actions
- Prometheus
- Grafana
- Loki

## Architecture Principles
- Public exposure minimized to ALB only
- Application and data services remain private
- Multi-AZ design for resilience
- Asynchronous processing for decoupling and fault tolerance
- Infrastructure fully reproducible through Terraform
- Observability included as a first-class concern

## 15-Day Build Plan
- [√] Day 1 - Define scope and lock architecture
- [ ] Day 2 - Terraform module structure
- [ ] Day 3 - Networking and foundational AWS resources
- [ ] Day 4 - EKS cluster provisioning
- [ ] Day 5 - Cluster platform components
- [ ] Day 6 - API service
- [ ] Day 7 - Worker service
- [ ] Day 8 - Database, secrets, and Redis
- [ ] Day 9 - Kubernetes deployments
- [ ] Day 10 - CI pipeline
- [ ] Day 11 - CD pipeline and infra workflow
- [ ] Day 12 - Observability stack
- [ ] Day 13 - Resilience and failure drills
- [ ] Day 14 - Backup, recovery, and security review
- [ ] Day 15 - Documentation and interview packaging

## Cost and Cleanup Strategy
This project is designed as a production-style lab, not a permanently running environment. Cost will be controlled by using small development-sized resources, limiting idle time, and destroying nonessential infrastructure after testing sessions.

## Planned Components
- API service
- Worker service
- Notification service
- PostgreSQL as durable state store
- SQS with DLQ for async processing
- Redis for cache/idempotency
- S3 for artifacts
- Prometheus/Grafana/Loki for observability