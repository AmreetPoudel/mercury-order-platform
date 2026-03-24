# docs/architecture.md

## Use case

This architecture is designed as a production-style, end-to-end cloud platform project for SRE, DevOps, and Cloud roles. The use case is a containerized application running on EKS with synchronous API traffic, asynchronous background processing, persistent relational storage, caching, object storage, observability, and CI/CD.

The goal is to demonstrate that the system is built with controlled public exposure, private workload execution, multi-AZ resilience, and realistic operational thinking.

---

## Public/private separation

### Public

Only these components should be public:

* **Application Load Balancer (ALB)**
* **Public subnets**
* **Internet Gateway**

### Private

Everything else stays private:

* **EKS worker nodes**
* **application pods**
* **RDS PostgreSQL**
* **Redis / ElastiCache**
* **SQS access from workloads**
* **S3 access from workloads**
* **monitoring stack**
* **internal service-to-service traffic**

### Design principle

If more than this is exposed, the design gets sloppy fast. Public exposure should be intentional, minimal, and justified. Least privilege is not a slogan here; it is part of the architecture.

---

## Data flow

### North-south traffic

User request flow:

`User -> ALB -> Ingress -> API Service`

This is the only internet-facing application entry path.

### East-west traffic

Internal service communication:

* `API Service -> PostgreSQL`
* `API Service -> SQS`
* `API Service -> Redis`
* `Worker Service -> SQS`
* `Worker Service -> PostgreSQL`
* `Worker Service -> S3`
* `Worker Service -> Redis`
* `Notification Service -> PostgreSQL` or internal event path, depending on final implementation

### Observability flow

* **Prometheus** scrapes application and cluster metrics
* **Loki** collects logs from cluster workloads
* **Grafana** visualizes metrics and logs

### CI/CD flow

`GitHub Actions -> ECR -> EKS`

The pipeline builds images, pushes to ECR, and deploys to EKS.

---

## AZ failure behavior

This architecture runs across **2 Availability Zones**.

### Spread across both AZs

* public subnets
* private app subnets
* private DB subnets
* EKS nodes
* ALB targets
* RDS Multi-AZ

### Expected behavior if one AZ fails

* **ALB** continues serving traffic through the remaining healthy AZ
* **EKS** reschedules pods onto healthy nodes in the surviving AZ, assuming enough spare capacity exists
* **API service** remains reachable if replicas are spread across zones
* **Worker service** continues if replicas are spread across zones
* **RDS Multi-AZ** fails over to the standby instance
* **SQS** remains available as a managed regional service
* **Redis** is treated as a managed available service for now, but should still be documented as a potential degradation point
* **Monitoring** may partially degrade if capacity planning is too tight

### What can still hurt during a one-AZ failure

* insufficient node capacity in the surviving AZ
* temporary interruption during DB failover
* too few pod replicas
* weak or missing pod anti-affinity rules
* badly configured PodDisruptionBudgets
* single NAT Gateway design used as a shortcut
* cost-cutting decisions that quietly reduce HA

That is where most fake “production-ready” designs collapse. They claim HA, but they have not actually thought through capacity, placement, and failover behavior.

---

## 5. Architecture Diagram v1

```text
                        Internet
                           |
                    +---------------+
                    |  AWS ALB      |
                    |  (Public)     |
                    +-------+-------+
                            |
                        Ingress
                            |
          ------------------------------------------------
          |                                              |
+---------------------+                       +---------------------+
| EKS Node Group AZ-A |                       | EKS Node Group AZ-B |
| Private App Subnet  |                       | Private App Subnet  |
+----------+----------+                       +----------+----------+
           |                                             |
   +-------+--------+                           +--------+-------+
   | API Service    |                           | Worker Service |
   | Notification   |                           | API Replicas   |
   +-------+--------+                           +--------+-------+
           |                                             |
           |------------------- Internal ----------------|
                           |
         -------------------------------------------------------
         |                    |                    |            |
         v                    v                    v            v
+----------------+   +----------------+   +----------------+  +------------------+
| RDS PostgreSQL |   | SQS Main Queue |   | ElastiCache    |  | S3 Artifacts     |
| Multi-AZ       |   | + DLQ          |   | Redis          |  | Bucket           |
| Private DB     |   | Managed        |   | Managed        |  | Managed          |
+----------------+   +----------------+   +----------------+  +------------------+

                           |
                    +---------------+
                    | Observability |
                    | Prometheus    |
                    | Grafana       |
                    | Loki          |
                    +---------------+

                           |
                    +---------------+
                    | GitHub Actions|
                    | CI/CD         |
                    +-------+-------+
                            |
                         ECR / EKS
```

---

## Design decisions

* Only the ALB is internet-facing; workloads and data services remain private.
* EKS worker nodes run in private subnets across two AZs.
* PostgreSQL runs on RDS Multi-AZ for database availability.
* Redis is used as a managed cache / fast-access store.
* SQS with DLQ is used to decouple background processing and absorb spikes.
* S3 is used for artifacts or generated files.
* Prometheus, Grafana, and Loki provide observability inside the private environment.
* GitHub Actions deploys through ECR into EKS.
* Least privilege is enforced at network and IAM level.
* High availability is designed around multi-AZ placement, replica distribution, and managed services.

---

## Security position

### Core security choices

* public exposure limited to ALB only
* workloads run in private subnets
* IAM roles for service access
* secrets should be stored outside code and manifests
* security groups restricted by actual traffic needs
* internal communication kept private by default

### What not to do

* do not expose worker, DB, Redis, Grafana, or internal services publicly
* do not use broad `0.0.0.0/0` access where targeted SG rules are enough
* do not collapse public and private boundaries for convenience
* do not pretend “private subnet” alone equals security

---

## 8. Failure Thinking

A serious architecture draft always answers this question: **what breaks first?**

Likely weak points:

1. **capacity exhaustion in surviving AZ** after one-AZ failure
2. **database failover pause** during RDS role switch
3. **Redis dependency creep** if application design becomes too reliant on cached state
4. **misconfigured Kubernetes placement rules** preventing healthy rescheduling
5. **single NAT design** becoming a hidden SPOF if cost is prioritized badly
6. **under-sized observability stack** during load or incident conditions

This matters in interviews because most people can list services. Very few can explain failure behavior honestly.

---

## 9. Cost and Cleanup Notes

### Cost-sensitive areas

* EKS control plane and worker node sizing
* NAT Gateway count
* RDS instance class and storage
* ElastiCache sizing
* observability retention and storage

### Cleanup strategy

* provision everything with Terraform
* tag all resources clearly
* keep state and module boundaries clean
* destroy nonessential environments quickly after validation
* retain only the minimal artifacts needed for demo and documentation

Do not lie to yourself here. “Production-style” does not mean “leave expensive managed services running forever.” It means build it cleanly enough that you can create, test, destroy, and recreate without chaos.

---

## Summary

This v1 architecture is intentionally opinionated:

* one controlled public entry point
* everything sensitive stays private
* two-AZ design with real failover thinking
* managed services used where they reduce risk
* asynchronous processing through SQS
* clear observability layer
* CI/CD integrated from the start

This is not the final architecture. It is the first architecture that is stable enough to build on without thrashing.
