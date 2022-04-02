DC := "docker-compose"

PROD="prod"
DEV="dev"
TEST="test"

PROJECT_NAME := "my_vocab_backend"
PROD_PROJECT_NAME := "${PROJECT_NAME}_${PROD}"
DEV_PROJECT_NAME := "${PROJECT_NAME}_${DEV}"
TEST_PROJECT_NAME := "${PROJECT_NAME}_${TEST}"

PROD_COMPOSE := "${DC}.${PROD}.yaml"
DEV_COMPOSE := "${DC}.${DEV}.yaml"
TEST_COMPOSE := "${DC}.${TEST}.yaml"

MIGRATIONS_DIR := "./app/db/migrations/versions"


prod:
	${DC} -f ${PROD_COMPOSE} --project-name ${PROD_PROJECT_NAME} up
prod-down:
	${DC} -f ${PROD_COMPOSE} --project-name ${PROD_PROJECT_NAME} down -v --rmi local

dev:
	${DC} -f ${DEV_COMPOSE} --project-name ${DEV_PROJECT_NAME} up
dev-down:
	${DC} -f ${DEV_COMPOSE} --project-name ${DEV_PROJECT_NAME} down -v --rmi local

test:
	${DC} -f ${TEST_COMPOSE} --project-name ${TEST_PROJECT_NAME} up
test-down:
	${DC} -f ${TEST_COMPOSE} --project-name ${TEST_PROJECT_NAME} down -v --rmi local

lint:
	flake8 app && \
	flake8 tests && \
	mypy app && \
	mypy tests --disable-error-code=override --disable-error-code=misc --disable-error-code=no-untyped-def

rm-mypy-cache:
	rm -rf .mypy_cache

clean:
	make prod-down
	make dev-down
	make test-down
	make rm-mypy-cache

migration:  # arguments: message: str;
	alembic revision --autogenerate -m ${message}

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade base

rm-migrations:
	rm ${MIGRATIONS_DIR}/*

dangerous-remigrate:
	make downgrade
	make rm-migrations
	make migration message="init"
	make migrate
