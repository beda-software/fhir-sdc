![example workflow](https://github.com/beda-software/fhir-sdc/actions/workflows/github-actions.yml/badge.svg)
# SDC spec implementation as microservice

The whole SDC specification you can find here http://hl7.org/fhir/uv/sdc/

## Upgrading to 3.x.x

`CONSTRAINT_LEGACY_BEHAVIOR` and `EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR` are gone, and both now behave as `False` did:

- an `itemConstraint` expression states what must hold, and the submission is refused when it evaluates to false.
  Expressions written for the legacy behaviour describe the error instead, and have to be negated;
- source queries are loaded for the constraint check only, so mappers receive the `$extract` parameters alone.

Setting either variable no longer has any effect.

`JUTE_SERVICE=aidbox` is gone too: JUTE mappers always run through a JUTE service, and the app refuses to start while
the variable still says `aidbox`. Leaving `JUTE_SERVICE` or `FHIRPATH_MAPPING_SERVICE` unset is fine — extraction then
refuses only the mappers that would have needed the missing service.

The FHIR server app now runs every query as the caller: it forwards the request's own credentials and no longer
reads `AUTH_TOKEN`. Callers need read access to `Questionnaire` and `StructureMap`, or `$populate`, `$assemble` and
`$extract` start refusing callers that could use them before.

The Aidbox app does the same: callers need read access to `Questionnaire` and `Mapping`.

## Access policies

fhir-sdc makes every request with the caller's credentials, so the caller needs policies for:

- `GET /fhir/Questionnaire/{id}/$assemble`
- `POST /fhir/Questionnaire/$populate`, `POST /fhir/Questionnaire/{id}/$populate`
- `POST /fhir/Questionnaire/$extract`, `POST /fhir/Questionnaire/{id}/$extract`
- `POST /fhir/QuestionnaireResponse/$constraint-check`
- `GET /fhir/Questionnaire?_id={id}` — the Questionnaire, and its sub-Questionnaires as `_id={id},{id}`
- `GET /fhir/Questionnaire?url={url}` (`&version={version}`) — a QuestionnaireResponse's Questionnaire
- `GET /fhir/Mapping?_id={id}` — the mappers
- `GET /fhir/StructureMap?_id={id}` — the mappers, in the FHIR server app only
- `POST /fhir` — `Questionnaire/$extract` submits the extraction

Anything else depends on the forms: context references, source queries and the resources the mappers write need the
policies the caller would need to reach them directly. Organization-scoped routes use the same paths under
`/Organization/{org_id}`. The test seeds in `initBundle.json` grant this list, bar `StructureMap`: the operations and
`POST /fhir` to anyone, the searches to the `sdc` Client.

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
