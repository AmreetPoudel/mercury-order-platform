#!/bin/bash

set -e

sudo apt update -y

sudo apt install -y \
    docker.io \
    docker-compose \
    git

sudo systemctl enable docker
sudo systemctl start docker

usermod -aG docker ubuntu

mkdir -p /home/ubuntu/mercury-order-platform

sudo chown ubuntu:ubuntu /home/ubuntu/mercury-order-platform