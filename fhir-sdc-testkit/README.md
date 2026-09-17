# fhir-sdc-testkit

Test an SDC Questionnaire and its Mapping the way a form is really filled: `$populate` runs, answers are placed at
each `linkId`'s nesting, the QuestionnaireResponse is saved, then `$extract` runs — checking `itemConstraint`s and
raising `OperationOutcome` on a violation. Only what a user types (or the frontend calculates) is faked;
`initialExpression`, source queries, constraints and the Mapping run against a real [fhir-sdc](../README.md) server.

```sh
pip install fhir-sdc-testkit
```

It is released from the same tag as the server, so install the version you run:
`fhir-sdc-testkit==3.1.0` goes with `bedasoftware/fhir-sdc:3.1.0`.

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
        parameters=launch_context({"Patient": patient}),
        answers={"postal-code": [answer(valueString="75001")]},
    )

    updated = await fhir_client.get(r4b.Patient, patient.id)
    assert updated.address[0].postalCode == "75001"
```

`populate_and_extract` returns the saved QuestionnaireResponse that the extraction ran on. Assert on the resources the
Mapping produced by fetching them from the server.

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

`parameters` is passed verbatim to `$populate` and merged into the `$extract` call, so anything the server accepts can
go in it. `launch_context()` builds the common case — a resource or a `Reference` under each context name:

```python
parameters=launch_context({"Patient": patient, "Author": r4b.Reference(reference="Practitioner/1")})
```

A list under a name builds one `context` parameter per resource, but the server keeps only the last of them —
until that is fixed, treat the list form as unsupported.

Add anything else by building the `Parameters` yourself:

```python
parameters=r4b.Parameters(parameter=[
    *launch_context({"Patient": patient}).parameter,
    r4b.ParametersParameter(name="subject", valueReference=r4b.Reference(reference=f"Patient/{patient.id}")),
])
```

## Constraint violations

```python
with pytest.raises(OperationOutcome) as refused:
    await populate_and_extract(fhir_client, "patient-intake", answers=answers)
assert refused.value.resource["issue"][0]["code"] == "postal-code-required"
```

## Development

```sh
uv sync
uv run pytest
uv run ruff format . && uv run ruff check . && uv run mypy
```

That suite covers answer placement without a server. `$populate`, constraints and extraction are covered against a
running Aidbox and SDC by `tests/testkit/` in the repository root — `./run_test.sh tests/testkit`.
