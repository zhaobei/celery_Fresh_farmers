#!/bin/bash
CONTAINER_NAME=celery_fresh
DOCKER_IMAGE=celery_fresh:latest

# Start Gunicorn processes
echo Starting Gunicorn.
function run {
  docker run -it \
    --name $CONTAINER_NAME \
    -v ${PWD}/config:/app/config:ro \
    -v ${PWD}/logs:/app/logs \
    -d \
    $DOCKER_IMAGE
}

docker rm -f $CONTAINER_NAME
run

