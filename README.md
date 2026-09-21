![example workflow](https://github.com/beda-software/fhir-sdc/actions/workflows/github-actions.yml/badge.svg)
# SDC spec implementation as microservice

The whole SDC specification you can find here http://hl7.org/fhir/uv/sdc/

## Using with Aidbox

In order to use extraction on behalf of the user, the Aidbox should be configured with `box_features_mapping_enable__access__control=true` environment variable.

## Upgrading to 3.x.x

`CONSTRAINT_LEGACY_BEHAVIOR` and `EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR` are gone, and both now behave as `False` did:

- an `itemConstraint` expression states what must hold, and the submission is refused when it evaluates to false.
  Expressions written for the legacy behaviour describe the error instead, and have to be negated;
- source queries are loaded for the constraint check only, so mappers receive the `$extract` parameters alone.

Setting either variable no longer has any effect.

## Further plans:
- JUTE-based population
- Observation-based population
- Observation-based extraction
- Definition-based extraction


## Tests
To run tests locally, copy `.env.tpl` to `.env` and specify `TESTS_AIDBOX_LICENSE`.  


Build images using `docker compose -f docker-compose.tests.yaml build`.


After that, just start `./run_test.sh` or `./run_test.sh tests/test_base.py` (if you want to run the particular file/test).
The first run may take about a minute because it prepares the db and devbox.


If you have updated some requirements, you need to re-run `docker compose -f docker-compose.tests.yaml build`
