from unittest.mock import MagicMock

import pytest
from fhirpy.base.exceptions import OperationOutcome

from app.sdc.utils import (
    build_fhirpath_env,
    is_sdc_api,
    normalize_answer_value,
    parse_parameters,
    prepare_bundle,
    prepare_link_ids,
    resolve_expression,
    resolve_fpml_template,
    resolve_questionnaire,
    resolve_string_template,
)
from app.utils import build_user_client
from tests.factories import create_questionnaire


def test_prepare_bundle_undefined_context():
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "/QuestionnaireResponse?subject={{%CurrentAppointmentId}}",
        }
    }

    with pytest.raises(ValueError, match="undefined environment variable"):
        prepare_bundle(bundle_entry, {})


def test_prepare_bundle():
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "/QuestionnaireResponse?subject={{%CurrentAppointmentId}}",
        }
    }

    assert prepare_bundle(bundle_entry, {"CurrentAppointmentId": None}) == {
        "request": {
            "method": "GET",
            "url": "/QuestionnaireResponse?subject=",
        }
    }


def test_prepare_bundle_encode_params():
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "/Patient?email={{%QuestionnaireResponse.repeat(item).where(linkId='email').answer.valueString}}",
        }
    }

    questionnaire_response = {
        "resourceType": "QuestionnaireResponse",
        "status": "final",
        "item": [
            {
                "linkId": "email",
                "answer": [
                    {
                        "valueString": "test+1@example.com",
                    }
                ],
            }
        ],
    }

    assert prepare_bundle(bundle_entry, {"QuestionnaireResponse": questionnaire_response}) == {
        "request": {
            "method": "GET",
            "url": "/Patient?email=test%2B1%40example.com",
        }
    }


def test_multuple_var_in_one_line():
    # Ref https://github.com/beda-software/aidbox-sdc/issues/1
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "Slot?specialty={{%specialty}}&start={{%start}}&status=free",
        }
    }

    env = {
        "specialty": "394586005",  # Gynecology
        "start": "2021-01-01",
    }
    assert prepare_bundle(bundle_entry, env) == {
        "request": {
            "method": "GET",
            "url": "Slot?specialty=394586005&start=2021-01-01&status=free",
        }
    }


def test_prepare_link_ids_does_not_encode_params():
    questionnaire = {
        "resourceType": "Questionnaire",
        "status": "active",
        "extension": [
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembleContext",
                "extension": [
                    {"url": "name", "valueString": "prefix"},
                    {"url": "type", "valueString": "string"},
                ],
            }
        ],
        "item": [
            {
                "linkId": "{{%prefix}}line-1",
                "type": "string",
            },
            {
                "linkId": "{{%prefix}}line-2",
                "type": "string",
                "enableWhen": [
                    {
                        "question": "{{%prefix}}line-1",
                        "operator": "exists",
                        "answerBoolean": True,
                    }
                ],
            },
        ],
    }

    assert prepare_link_ids(questionnaire, {"prefix": "test+"}) == {
        "extension": [
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembleContext",
                "extension": [
                    {"url": "name", "valueString": "prefix"},
                    {"url": "type", "valueString": "string"},
                ],
            }
        ],
        "item": [
            {"linkId": "test+line-1", "type": "string"},
            {
                "enableWhen": [
                    {
                        "answerBoolean": True,
                        "operator": "exists",
                        "question": "test+line-1",
                    }
                ],
                "linkId": "test+line-2",
                "type": "string",
            },
        ],
        "resourceType": "Questionnaire",
        "status": "active",
    }


@pytest.mark.parametrize(
    ("answer_type", "values", "expected"),
    [
        ("string", ["abc", "dfe", "htd"], "/Patient?_id=abc,dfe,htd"),
        ("number", [1, 4, 5], "/Patient?_id=1,4,5"),
        ("string", ["single-id"], "/Patient?_id=single-id"),
        ("number", [5], "/Patient?_id=5"),
    ],
)
def test_resolve_string_template(answer_type, values, expected):
    questionnaire_response = {
        "resourceType": "QuestionnaireResponse",
        "item": [
            {
                "linkId": "patients-group",
                "item": [
                    {
                        "linkId": "patients-set",
                        "answer": [{"value": {answer_type: value}} for value in values],
                    }
                ],
            }
        ],
    }
    template_input = (
        "/Patient?_id={{%QuestionnaireResponse.repeat(item).where(linkId='patients-set').answer.children()."
        + answer_type
        + "}}"
    )
    result = resolve_string_template(
        {}, template_input, {"QuestionnaireResponse": questionnaire_response}
    )
    assert result == expected


def test_fpml():
    questionnaire_response = {
        "resourceType": "QuestionnaireResponse",
        "item": [
            {
                "linkId": "patients-group",
                "item": [
                    {
                        "linkId": "patientId",
                        "answer": [{"valueString": "1"}],
                    }
                ],
            }
        ],
    }
    template = {
        "resourceType": "Patient",
        "id": "{{ %QuestionnaireResponse.answers('patientId') }}",
    }
    result = resolve_fpml_template(template, {"QuestionnaireResponse": questionnaire_response})
    assert result == {"resourceType": "Patient", "id": "1"}


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        (None, False),
        ({}, False),
        ({"resourceType": "Patient", "id": "x"}, False),
        ({"resourceType": "Parameters", "parameter": []}, False),
        (
            {
                "resourceType": "Parameters",
                "parameter": [{"name": "questionnaire", "resource": {}}],
            },
            False,
        ),
        (
            {
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "Questionnaire", "resource": {}},
                    {"name": "LaunchPatient", "resource": {"resourceType": "Patient"}},
                ],
            },
            False,
        ),
        (
            {
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "subject", "valueReference": {"reference": "Patient/1"}},
                ],
            },
            True,
        ),
        (
            {
                "resourceType": "Parameters",
                "parameter": [{"name": "context", "part": []}],
            },
            True,
        ),
        (
            {
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "context", "part": []},
                    {"name": "subject", "valueReference": {"reference": "Patient/1"}},
                ],
            },
            True,
        ),
    ],
)
def test_is_sdc_api(payload, expected):
    assert is_sdc_api(payload) is expected


@pytest.mark.parametrize(
    "launch_param",
    [
        {"name": "launch-patientId", "valueString": "patient-123"},
    ],
)
async def test_parse_parameters_splits_parameters(launch_param):
    client = MagicMock()
    questionnaire = {
        "resourceType": "Questionnaire",
        "id": "q-1",
        "status": "active",
    }
    questionnaire_response = {
        "resourceType": "QuestionnaireResponse",
        "id": "qr-1",
        "status": "completed",
    }
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "questionnaire", "resource": questionnaire},
            {"name": "questionnaire_response", "resource": questionnaire_response},
            launch_param,
        ],
    }

    parsed = await parse_parameters(client, parameters)
    assert parsed == (questionnaire, questionnaire_response, {"launch-patientId": "patient-123"})


@pytest.mark.parametrize("name", ["questionnaire", "Questionnaire"])
async def test_parse_parameters_accepts_every_questionnaire_spelling(name):
    questionnaire = {"resourceType": "Questionnaire", "id": "q-1"}
    parameters = {
        "resourceType": "Parameters",
        "parameter": [{"name": name, "resource": questionnaire}],
    }

    parsed = await parse_parameters(MagicMock(), parameters)
    assert parsed == (questionnaire, None, {})


@pytest.mark.parametrize(
    "name", ["questionnaire-response", "questionnaire_response", "QuestionnaireResponse"]
)
async def test_parse_parameters_accepts_every_questionnaire_response_spelling(name):
    questionnaire_response = {"resourceType": "QuestionnaireResponse", "id": "qr-1"}
    parameters = {
        "resourceType": "Parameters",
        "parameter": [{"name": name, "resource": questionnaire_response}],
    }

    parsed = await parse_parameters(MagicMock(), parameters)
    assert parsed == (None, questionnaire_response, {})


def test_build_fhirpath_env_exposes_every_alias():
    questionnaire = {"resourceType": "Questionnaire", "id": "q-1"}
    questionnaire_response = {"resourceType": "QuestionnaireResponse", "id": "qr-1"}

    env = build_fhirpath_env(questionnaire, questionnaire_response, {"subject": {"id": "p-1"}})
    assert env == {
        "subject": {"id": "p-1"},
        "Questionnaire": questionnaire,
        "questionnaire": questionnaire,
        "QuestionnaireResponse": questionnaire_response,
        "questionnaire_response": questionnaire_response,
        "resource": questionnaire_response,
    }


def test_build_fhirpath_env_without_questionnaire_response():
    questionnaire = {"resourceType": "Questionnaire", "id": "q-1"}

    env = build_fhirpath_env(questionnaire, None, {})
    assert env == {"Questionnaire": questionnaire, "questionnaire": questionnaire}


async def test_parse_parameters_skips_empty_launch_param():
    client = MagicMock()
    questionnaire = {
        "resourceType": "Questionnaire",
        "id": "q-1",
        "status": "active",
    }
    questionnaire_response = {
        "resourceType": "QuestionnaireResponse",
        "id": "qr-1",
        "status": "completed",
    }
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "questionnaire", "resource": questionnaire},
            {"name": "questionnaire_response", "resource": questionnaire_response},
            {"name": "launch-patientId", "value": {}},
        ],
    }

    parsed = await parse_parameters(client, parameters)
    assert parsed == (questionnaire, questionnaire_response, {})


@pytest.mark.asyncio
async def test_parse_parameters_resolves_context_reference(fhir_client, safe_db):
    obs = fhir_client.resource(
        "Observation",
        status="final",
        code={"text": "parameter-to-env-integration"},
    )
    await obs.save()

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "context",
                "part": [
                    {"name": "name", "valueString": "Observation"},
                    {
                        "name": "content",
                        "valueReference": {"reference": f"Observation/{obs.id}"},
                    },
                ],
            },
        ],
    }

    _, _, variables = await parse_parameters(fhir_client, parameters)

    assert is_sdc_api(parameters) is True
    resolved = variables["Observation"]
    assert resolved["resourceType"] == "Observation"
    assert resolved["id"] == obs.id
    assert resolved["status"] == "final"
    assert resolved["code"]["text"] == "parameter-to-env-integration"


@pytest.mark.asyncio
async def test_parse_parameters_resolves_subject_reference(fhir_client, safe_db):
    patient = fhir_client.resource("Patient")
    await patient.save()
    patient_ref = {"reference": f"Patient/{patient.id}"}

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "subject", "valueReference": patient_ref},
        ],
    }

    _, _, variables = await parse_parameters(fhir_client, parameters)

    assert is_sdc_api(parameters) is True
    assert variables["subject"]["resourceType"] == "Patient"
    assert variables["subject"]["id"] == patient.id


@pytest.mark.asyncio
async def test_parse_parameters_does_not_resolve_non_subject_reference(fhir_client, safe_db):
    # This test for backward compatibility with non sdc api behavior
    patient = fhir_client.resource("Patient")
    await patient.save()
    patient_ref = {"reference": f"Patient/{patient.id}", "display": "Integration Patient"}

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "PatientRef", "valueReference": patient_ref},
        ],
    }

    _, _, variables = await parse_parameters(fhir_client, parameters)

    assert is_sdc_api(parameters) is False
    assert variables["PatientRef"]["display"] == "Integration Patient"
    assert variables["PatientRef"]["reference"] == f"Patient/{patient.id}"


@pytest.mark.asyncio
async def test_sdc_api_params(fhir_client, safe_db):
    patient = fhir_client.resource(
        "Patient",
        name=[{"family": "ApiParams", "given": ["SdcIntegration"]}],
    )
    await patient.save()

    questionnaire = {
        "resourceType": "Questionnaire",
        "id": "q-sdc-api-params",
        "status": "active",
    }

    patient_ref = {
        "reference": f"Patient/{patient.id}",
        "display": "Integration Patient",
    }

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "questionnaire", "resource": questionnaire},
            {
                "name": "context",
                "part": [
                    {"name": "name", "valueString": "Patient"},
                    {"name": "content", "valueReference": patient_ref},
                ],
            },
        ],
    }

    _, _, variables = await parse_parameters(fhir_client, parameters)

    assert is_sdc_api(parameters) is True
    resolved = variables["Patient"]
    assert resolved["resourceType"] == "Patient"
    assert resolved["id"] == patient.id
    assert resolved["name"][0]["family"] == "ApiParams"
    assert resolved["name"][0]["given"] == ["SdcIntegration"]


@pytest.mark.asyncio
async def test_sdc_api_params_with_resource(fhir_client, safe_db):
    patient = {
        "resourceType": "Patient",
        "name": [{"family": "ApiParams", "given": ["SdcIntegration"]}],
    }

    questionnaire = {
        "resourceType": "Questionnaire",
        "id": "q-sdc-api-params",
        "status": "active",
    }

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "questionnaire", "resource": questionnaire},
            {
                "name": "context",
                "part": [
                    {"name": "name", "valueString": "Patient"},
                    {"name": "content", "resource": patient},
                ],
            },
        ],
    }

    _, _, variables = await parse_parameters(fhir_client, parameters)

    assert is_sdc_api(parameters) is True
    resolved = variables["Patient"]
    assert resolved["resourceType"] == "Patient"
    assert resolved["name"][0]["family"] == "ApiParams"
    assert resolved["name"][0]["given"] == ["SdcIntegration"]


@pytest.mark.asyncio
async def test_x_fhir_query_variable(fhir_client, safe_db):
    patient = fhir_client.resource(
        "Patient",
        name=[{"family": "ApiParams", "given": ["SdcIntegration"]}],
    )
    await patient.save()
    env = {"patient": patient}
    expression = {
        "name": "MedicationStatement",
        "language": "application/x-fhir-query",
        "expression": "MedicationStatement?patient={{%patient.id}}&status=active&_include=MedicationStatement:medication",
    }
    result = await resolve_expression(fhir_client, {}, expression, env, "test")
    assert result["resourceType"] == "Bundle"


@pytest.mark.asyncio
async def test_x_fhir_query_variable_escape(fhir_client, safe_db):
    name = "MrX&active=false"
    patient = fhir_client.resource(
        "Patient",
        active=True,
        name=[{"text": name}],
    )
    await patient.save()
    env = {"patient": patient}
    expression = {
        "name": "MedicationStatement",
        "language": "application/x-fhir-query",
        "expression": "Patient?name={{%patient.name.text}}",
    }
    result = await resolve_expression(fhir_client, {}, expression, env, "test")
    assert result["resourceType"] == "Bundle"
    assert result["total"] == 1


LOCATION = {"resourceType": "Location", "id": "location-1", "name": "Location 1"}


def test_normalize_answer_value_resource_to_reference_with_display():
    assert normalize_answer_value("Reference", LOCATION, "Location.name") == {
        "reference": "Location/location-1",
        "display": "Location 1",
    }


def test_normalize_answer_value_resource_to_reference_without_display_path():
    assert normalize_answer_value("Reference", LOCATION) == {"reference": "Location/location-1"}


def test_normalize_answer_value_omits_display_when_path_finds_nothing():
    assert normalize_answer_value("Reference", LOCATION, "alias") == {
        "reference": "Location/location-1"
    }


def test_normalize_answer_value_omits_non_string_display():
    assert normalize_answer_value("Reference", LOCATION, "name.exists()") == {
        "reference": "Location/location-1"
    }


def test_normalize_answer_value_keeps_reference_as_is():
    reference = {"reference": "Location/location-1"}

    assert normalize_answer_value("Reference", reference, "Location.name") == reference


def test_user_client_forwards_only_the_callers_own_headers():
    headers = {
        "Authorization": "Bearer caller-token",
        "x-correlation-id": "abc",
        "Host": "fhir-sdc.example",
        "content-length": "42",
        "Transfer-Encoding": "chunked",
    }

    client = build_user_client(headers, "http://ehr.example/fhir")
    assert client.url == "http://ehr.example/fhir"
    assert client.authorization is None
    assert client.extra_headers == {
        "Authorization": "Bearer caller-token",
        "x-correlation-id": "abc",
    }


@pytest.mark.asyncio
async def test_resolve_questionnaire_requires_a_canonical(fhir_client, safe_db):
    with pytest.raises(OperationOutcome, match="`questionnaire` is required"):
        await resolve_questionnaire(fhir_client, None)


@pytest.mark.asyncio
async def test_resolve_questionnaire_reports_an_unknown_canonical(fhir_client, safe_db):
    with pytest.raises(OperationOutcome, match="is not found"):
        await resolve_questionnaire(fhir_client, "http://example.com/Questionnaire/missing")


@pytest.mark.asyncio
async def test_resolve_questionnaire_refuses_an_ambiguous_canonical(fhir_client, safe_db):
    url = "http://example.com/Questionnaire/versioned"
    await create_questionnaire(fhir_client, {"status": "active", "url": url, "version": "1.0"})
    await create_questionnaire(fhir_client, {"status": "active", "url": url, "version": "2.0"})

    with pytest.raises(OperationOutcome, match="several versions"):
        await resolve_questionnaire(fhir_client, url)
