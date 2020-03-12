source .env

function run {
  docker run \
    --name $CONTAINER_NAME \
    -p 8000:8000 \
    -v ${PWD}/config.toml:/app/config.toml:ro \
    -d \
    $DOCKER_IMAGE \
    bash run.sh
}

if
  docker pull $DOCKER_IMAGE
then
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
  run
fi
