start:
	while ! nc -z ${POSTGRES_HOST} ${DOCKER_DB_PORT}; do sleep 0.1; done
	while ! nc -z ${REDIS_HOST} ${REDIS_PORT}; do sleep 0.1; done
	alembic upgrade head
	python -m gunicorn --name url_service -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000 main:app