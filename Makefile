DOCKER_DEV=docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml
DOCKER_TEST=docker-compose -f docker-compose.yaml -f docker-compose.test.yaml
DOCKER_ADMIN=docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml -f docker-compose.admin.yaml
DOCKER_PROD=docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml

ENV=DEV
CONT=web

up:
	$(DOCKER_$(ENV)) up

build:
	$(DOCKER_$(ENV)) build

bash:
	$(DOCKER_$(ENV)) run --rm $(CONT) bash

test:
	$(DOCKER_TEST) up

lint:
	$(DOCKER_TEST) run --rm web tox -e lint

user:
	$(DOCKER_TEST) run --rm web /app/venv/bin/python /app/manage.py createsuperuser