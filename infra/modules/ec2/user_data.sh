#!/bin/bash

set -e

apt update -y

apt install -y \
    docker.io \
    git \
    awscli

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

mkdir -p /home/ubuntu/mercury-order-platform

chown ubuntu:ubuntu /home/ubuntu/mercury-order-platform