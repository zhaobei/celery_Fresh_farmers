#!/bin/bash
CONTAINER_NAME=fresh
DOCKER_IMAGE=fresh:latest

# Start Gunicorn processes
echo Starting Gunicorn.
function run {
  docker run -it \
    --name $CONTAINER_NAME \
    -p 8000:8000 \
    -v ${PWD}/config:/app/config:ro \
    -v ${PWD}/logs:/app/logs \
    -d \
    $DOCKER_IMAGE
}

docker rm -f $CONTAINER_NAME
run

