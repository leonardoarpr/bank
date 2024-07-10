ifneq ("$(wildcard .env)","")
  $(info using .env)
  include .env
endif

CONTAINER_NAME=ebanx_app
COMPOSEV2 := $(shell docker compose version)

ifdef COMPOSEV2
    COMMAND=docker compose
else
    COMMAND=docker-compose
endif


docker-up:
	$(COMMAND) up -d

docker-down:
	$(COMMAND) down

docker-bash: docker-up
	docker exec -it $(CONTAINER_NAME) sh

docker-logs:
	docker-compose logs -f

test: docker-up
	docker exec -t $(CONTAINER_NAME) python -m unittest discover app/tests/unit

coverage-test: docker-up
	coverage run -m unittest discover ./app/tests/unit && coverage-badge -o coverage.svg

coverage-html: docker-up
	docker exec -t $(CONTAINER_NAME) python -m pytest --cov-report term-missing --cov=app/src/ --cov-fail-under=80  coverage-badge coverage.svg