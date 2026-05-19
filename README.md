📄 README.md (Manual Infrastructure Setup)
# Mercury Order Platform - Infrastructure & Deployment Guide

This guide explains how to initialize and run the system manually using Terraform + Docker Compose.

---

# 🧱 Architecture Overview

The system consists of:

- AWS VPC (public subnet)
- EC2 instance (application host)
- Security Group (HTTP, HTTPS, SSH, API ports)
- Elastic IP (stable public IP)
- PostgreSQL (container)
- Redis (container)
- FastAPI backend (containerized API)
- Worker (optional background service)

---

# ⚙️ Prerequisites

Install locally:

- Terraform
- AWS CLI configured
- Docker
- Docker Compose
- SSH key for EC2 access

---

# 🚀 Step 1: Infrastructure Provisioning (Terraform)

Navigate to environment:

```bash
cd infra/environments/dev

Initialize Terraform:

terraform init

Apply infrastructure:

terraform apply

Confirm with:

yes
📌 Output after apply

Terraform will output:

EC2 Public IP (Elastic IP)

Example:

ec2_public_ip = "13.xx.xx.xx"
🔐 Step 2: SSH into EC2
ssh -i mercury-key.pem ubuntu@<EC2_PUBLIC_IP>
🐳 Step 3: Install Docker (first time only)

On EC2:

sudo apt update -y
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo usermod -aG docker ubuntu
newgrp docker

Verify:

docker --version
docker compose version
📦 Step 4: Clone Project on EC2
git clone https://github.com/<your-repo>/mercury-order-platform.git
cd mercury-order-platform
⚙️ Step 5: Setup Environment File

Create .env on EC2:

nano .env

Example:

DATABASE_URL=postgresql://app:app@postgres:5432/orders
REDIS_HOST=redis

Save and exit.

🗄️ Step 6: Initialize Database (ONE TIME ONLY)

Run:

python apps/common/init_db.py

This will:

create tables
initialize schema in PostgreSQL
🚀 Step 7: Start System (Docker Compose)

Run:

docker compose up -d

Check running containers:

docker ps
🌐 Step 8: Access Application

FastAPI will be available at:

http://<EC2_PUBLIC_IP>:8000/docs
🔄 Step 9: Deployment Update Flow

When new version is pushed to DockerHub:

On EC2:

docker compose pull
docker compose up -d
🔁 Step 10: Rollback Strategy

To rollback:

Edit docker-compose.yaml:

image: aamreet/mercury-api:v1

Then:

docker compose up -d
🧠 Key Operational Principles
Infrastructure is immutable via Terraform
Application is deployed via containers
Images are versioned in DockerHub
.env controls runtime configuration
EC2 is only execution layer
⚠️ Important Notes
Do NOT commit .env
Do NOT store secrets in Docker images
Do NOT rely on latest tag in production
Always prefer versioned images (v1, v2, git SHA)
🧪 Health Check
curl http://localhost:8000/healthz
📌 Future Improvements (Optional)
CI/CD via GitHub Actions
Automated deployment via SSH
Elastic Load Balancer
HTTPS with Nginx + Certbot
Centralized logging


system reliability > code perfection
