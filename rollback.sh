#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Usage: ./rollback.sh <image_tag>"
  exit 1
fi

IMAGE_TAG=$1

export IMAGE_TAG=$IMAGE_TAG

echo "[ROLLBACK] using image tag: $IMAGE_TAG"

docker compose pull

docker compose up -d

echo "[ROLLBACK] completed"