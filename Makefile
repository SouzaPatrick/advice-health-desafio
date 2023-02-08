IMAGE_NAME=flask-advice-health
CONTAINER_NAME=flask-advice-health

## @ Project
.PHONY: install up generate_db down
install: generate_db build up # Generate the backend image and upload ALL containers in the project

up: ## Starts ALL containers in the project
	@docker-compose up -d

down: ## Stop ALL containers in the project
	@docker-compose down

build: ## Create flask image from project
	@docker build -t ${IMAGE_NAME}:latest .
	@sleep 10

generate_db: ## Create a SQLite database and add all tables in it
	@python generate_db.py

## @ Pre-commit
.PHONY: format
format:
	@pre-commit run --all-files

## @ Extras
.PHONY: test check_flask_running
test:
	@docker exec -i ${CONTAINER_NAME} sh -c "pytest -v --disable-pytest-warnings"

check_flask_running:
	@RUNNING=$$(docker ps -f name=${CONTAINER_NAME} --format="{{.ID}}"); \
	echo $${RUNNING}; \
	if [ "$${RUNNING}" = "" ]; then \
		echo "${CONTAINER_NAME} machine must be running to run this command"; \
		exit 1; \
	fi