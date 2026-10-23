# fhir-sdc-testkit

Test an SDC Questionnaire and its extraction the way a form is really filled: `$populate` runs, answers are placed at
each `linkId`'s nesting, the QuestionnaireResponse is saved, then `QuestionnaireResponse/$extract` runs and the
bundle it returns is submitted. Only what a user types (or the frontend calculates) is faked; everything else runs on
a real server implementing the [SDC](https://build.fhir.org/ig/HL7/sdc/) operations, such as
[fhir-sdc](../README.md).

```sh
pip install fhir-sdc-testkit
```

It is released from the fhir-sdc repository, with the same version as the fhir-sdc release it is tested against.

## The client

Everything takes an `AsyncFHIRClient` rooted at the server's `/fhir` base, built with `dump_resource` — fhirpy cannot
serialize pydantic resources without it:

```python
fhir_client = AsyncFHIRClient(
    f"{base_url}/fhir",
    authorization=authorization,
    dump_resource=lambda resource: resource.model_dump(),
)
```

## Usage

```python
import fhirpy_types_r4b as r4b
from fhir_sdc_testkit import answer, launch_context, populate_and_extract


async def test_intake_records_the_address(fhir_client):
    patient = await fhir_client.create(r4b.Patient(name=[r4b.HumanName(family="Test")]))

    await populate_and_extract(
        fhir_client,
        "patient-intake",
        parameters=launch_context(
            {"Patient": patient}, subject=r4b.Reference(reference=f"Patient/{patient.id}")
        ),
        answers={"postal-code": [answer(valueString="75001")]},
    )

    updated = await fhir_client.get(r4b.Patient, patient.id)
    assert updated.address[0].postalCode == "75001"
```

`populate_and_extract` returns the saved QuestionnaireResponse that the extraction ran on. Assert on the resources
the extraction produced by fetching them from the server.

### Answers

Keys are `linkId`s, addressed flatly — groups in between are created for you:

```python
answers={
    "country": [answer(valueCoding=r4b.Coding(code="FR"))],
    "postal-code": [answer(valueString="75001")],
}
```

A repeating group takes one answer set per occurrence, filled positionally over the occurrences `$populate` produced,
appending any that are missing and leaving extra populated ones alone:

```python
answers={
    "contacts": [
        {"phone": [answer(valueString="+1 555 0100")], "label": [answer(valueString="home")]},
        {"phone": [answer(valueString="+1 555 0111")], "label": [answer(valueString="work")]},
    ],
}
```

Inside a set, `linkId`s are flat again. A `linkId` that does not belong to the group raises, naming it.

### Parameters

`parameters` is required: it is passed to `$populate` and merged into the `$extract` call, so anything the server
accepts can go in it. `launch_context()` builds the SDC `$populate` input — a resource or a `Reference` under each
context name, and the optional `subject`. Pass at least one of them: a `$populate` reply that is not `Parameters`
raises `ValueError`.

```python
parameters=launch_context({"Patient": patient, "Author": r4b.Reference(reference="Practitioner/1")})
```

A list under a name builds one `context` with a `content` part per value, as SDC defines it. fhir-sdc uses only the
first `content` for now.

## Failures

An error response from the server raises fhirpy's exception for its status — `OperationOutcome` for most 4xx and 5xx
responses. A violated `itemConstraint` the server checks during `$extract` and a rejected transaction both arrive this
way; they differ in `issue[].code`. fhir-sdc reports a constraint's `key`, and a server's own validation code, such as
`invalid`, for a transaction. An `error` or `fatal` issue in the `$extract` result and a batch entry the server
rejects raise `ExtractionError`.

```python
with pytest.raises(OperationOutcome) as refused:
    await populate_and_extract(fhir_client, "patient-intake", parameters=parameters, answers=answers)
assert refused.value.resource["issue"][0]["code"] == "postal-code-required"
```

## Development

```sh
uv sync
uv run pytest
uv run ruff format . && uv run ruff check . && uv run mypy
```

That suite runs without a server. `$populate`, constraints and extraction are covered against a running Aidbox and
fhir-sdc by `tests/testkit/` in the repository root — `./run_test.sh tests/testkit`.
