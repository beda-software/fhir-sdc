#!/bin/sh

if [ -f ".env" ]; then
    export `cat .env`
fi

if [ -z "${TESTS_AIDBOX_LICENSE_KEY}" ]; then
    echo "TESTS_AIDBOX_LICENSE_KEY is required to run tests"
    exit 1
fi

if [ -z "${TESTS_AIDBOX_LICENSE_ID}" ]; then
    echo "TESTS_AIDBOX_LICENSE_ID is required to run tests"
    exit 1
fi

export TEST_COMMAND="pipenv run pytest --cov-report html --cov-report term:skip-covered --cov=main $@"


M1=`uname -a | grep -o arm64`

COMPOSE_FILES="-f docker-compose.tests.yaml"

docker-compose -f docker-compose.tests.yaml build
docker-compose $COMPOSE_FILES  up --exit-code-from backend backend
exit $?
