# Makefile for common commands

PYTHON=pipenv run python
PROJECT_HOME?=.
DOCKER_IMAGE=britecore_assignment
DOCKER_CONTAINER=britecore_api
HEROKU_APP_NAME=britecore-assignment

.DEFAULT: help

help:
	@echo "make test - To run test cases"
	@echo "make pretty - Does linting and deletes *.pyc files"
	@echo "make requirements - Makes requirements.txt"
	@echo "make testdeploy - Build and deploy docker container"


pretty:
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	isort -rc --atomic $(PROJECT_HOME)
	find . -type f -name "*.py" -exec $(PYTHON) -m yapf --recursive --parallel --in-place --verbose --style=pep8 {} \;
	find . -type f -name "*.py" -exec $(PYTHON) -m autoflake --recursive --in-place --remove-unused-variables --remove-all-unused-imports --exclude=__init__.py {} \;

test:
	$(PYTHON) -m unittest

requirements:
	$(PYTHON) -m pip freeze > requirements.txt

testdeploy:
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true
	docker rmi $(DOCKER_IMAGE) || true
	docker build -t $(DOCKER_IMAGE) .
	docker run --name $(DOCKER_CONTAINER) -d -e PORT=5000 -p 8000:5000 $(DOCKER_IMAGE):latest

deploy:
	heroku container:push web --app $(HEROKU_APP_NAME)
	heroku container:release web --app $(HEROKU_APP_NAME)
	heroku open --app $(HEROKU_APP_NAME)

logs:
	heroku logs --tail --app $(HEROKU_APP_NAME)

login:
	heroku run bash --app $(HEROKU_APP_NAME)

clean:
	docker images -q |xargs docker rmi
	docker ps -q |xargs docker rm
