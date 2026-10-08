#!/bin/sh

if [ -f ".env" ]; then
    export `cat .env`
fi

if [ -z "${TESTS_AIDBOX_LICENSE}" ]; then
    echo "TESTS_AIDBOX_LICENSE is required to run tests"
    exit 1
fi

export TEST_COMMAND="pytest --cov-report html:/tmp/htmlcov --cov-report term:skip-covered --cov=app $@"

COMPOSE_FILES="-f docker-compose.tests.yaml"

docker compose -f docker-compose.tests.yaml build
docker compose $COMPOSE_FILES  up --exit-code-from backend backend
exit $?
