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

export TEST_COMMAND=" wait-for-it.sh devbox:8080 --strict --timeout=0 -- pipenv run pytest --cov-report html --cov-report term:skip-covered --cov=main $@"


M1=`uname -a | grep -o arm64`

if [ -z "${M1}" ]; then
    COMPOSE_FILES="-f docker-compose.tests.yaml"
else
    COMPOSE_FILES="-f docker-compose.tests.yaml -f docker-compose.tests.m1.yaml"
fi

docker-compose $COMPOSE_FILES  up --exit-code-from backend backend
exit $?
