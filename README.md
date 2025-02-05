![example workflow](https://github.com/beda-software/fhir-sdc/actions/workflows/github-actions.yml/badge.svg)
# SDC spec implementation as microservice

The whole SDC specification you can find here http://hl7.org/fhir/uv/sdc/

## Using with Aidbox

In order to use extraction on behalf of the user, the Aidbox should be configured with `box_features_mapping_enable__access__control=true` environment variable.

## New projects setup

For new installations, you must specify the following environment variables:
```
CONSTRAINT_LEGACY_BEHAVIOR=False
CREATE_MANIFEST_ATTRS=False
```

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
