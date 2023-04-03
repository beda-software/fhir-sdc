![example workflow](https://github.com/beda-software/aidbox-sdc/actions/workflows/github-actions.yml/badge.svg)
# SDC spec implementation as Aidbox application

The whole SDC specification you can find here http://hl7.org/fhir/uv/sdc/2019May/index.html  

## WIP Features:  

- FHIRPath-based population http://hl7.org/fhir/uv/sdc/2019May/populate.html#fhirpath-based-population
- Assemble operation https://jira.hl7.org/browse/FHIR-22356
- JUTE-based extraction

## Further plans:
- Support FHIR resource format https://docs.aidbox.app/modules-1/fhir-resources/aidbox-and-fhir-formats
- JUTE-based population
- Observation-based population
- Observation-based extraction
- Definition-based extraction


## Tests
To run tests locally, copy `.env.tpl` to `.env` and specify `TESTS_AIDBOX_LICENSE_ID` and `TESTS_AIDBOX_LICENSE_KEY`.  


Build images using `docker-compose -f docker-compose.tests.yaml build`.


After that, just start `./run_test.sh` or `./run_test.sh tests/test_base.py` (if you want to run the particular file/test).
The first run may take about a minute because it prepares the db and devbox.


If you have updated some requirements, you need to re-run `docker-compose -f docker-compose.tests.yaml build`
