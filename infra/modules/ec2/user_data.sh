#!/bin/bash

set -eux

apt update -y

apt install -y \
    docker.io \
    docker-compose-v2 \
    git \
    unzip \
    curl

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip

unzip awscliv2.zip

./aws/install

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

mkdir -p /home/ubuntu/mercury-order-platform

chown -R ubuntu:ubuntu /home/ubuntu/mercury-order-platform