# Variables
ENV_FILE ?= .env.test
ALEMBIC := docker-compose exec app poetry run alembic
DOCKER_COMPOSE := docker-compose

# Help command
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make docker-up                        - Start the application in normal mode with Docker Compose"
	@echo "  make docker-debug                     - Start the application in debug mode with Docker Compose"
	@echo "  make docker-down                      - Stop the application and remove containers"
	@echo "  make docker-rebuild                   - Rebuild the Docker containers"
	@echo "  make docker-logs                      - View logs of the application"
	@echo "  make docker-app-shell                 - Open a shell inside the app container"
	@echo "  make revision MESSAGE=\"message\"      - Create a new migration with Alembic"
	@echo "  make upgrade                          - Apply the latest migrations"
	@echo "  make downgrade                        - Rollback the last migration"
	@echo "  make show                             - Display the current migration status"
	@echo "  make run                              - Start the FastAPI application locally"
	@echo "  make test                             - Run tests locally"

# Docker commands
.PHONY: docker-up
docker-up:
	@$(DOCKER_COMPOSE) --env-file $(ENV_FILE) up -d app

.PHONY: docker-debug
docker-debug:
	@$(DOCKER_COMPOSE) --env-file $(ENV_FILE) up -d app-debug

.PHONY: docker-down
docker-down:
	@$(DOCKER_COMPOSE) down

.PHONY: docker-rebuild
docker-rebuild:
	@$(DOCKER_COMPOSE) down
	@$(DOCKER_COMPOSE) --env-file $(ENV_FILE) up --build -d app

.PHONY: docker-logs
docker-logs:
	@$(DOCKER_COMPOSE) logs -f

.PHONY: docker-app-shell
docker-app-shell:
	@$(DOCKER_COMPOSE) exec app bash

# Alembic commands using Docker
.PHONY: revision
revision:
	@$(ALEMBIC) revision --autogenerate -m "$(MESSAGE)"

.PHONY: upgrade
upgrade:
	@$(ALEMBIC) upgrade head

.PHONY: downgrade
downgrade:
	@$(ALEMBIC) downgrade -1

.PHONY: show
show:
	@$(ALEMBIC) current

# Local FastAPI and Testing
.PHONY: run
run:
	@poetry run uvicorn app.main:app --reload

.PHONY: test
test:
	@poetry run pytest
