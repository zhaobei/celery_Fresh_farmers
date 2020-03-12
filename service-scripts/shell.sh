source .env
docker exec -it $CONTAINER_NAME pipenv run python manage.py shell
