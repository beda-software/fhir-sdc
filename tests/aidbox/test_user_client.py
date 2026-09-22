import base64

import pytest
from fhirpy import AsyncFHIRClient
from fhirpy.base.exceptions import BaseFHIRError

from app.aidbox.utils import rebuild_at_external_fhir_base_url
from tests.factories import create_questionnaire, make_questionnaire_mapper_ext


def test_user_client_moves_only_when_the_request_names_an_external_server():
    user_client = AsyncFHIRClient(
        "http://aidbox:8080/fhir", extra_headers={"Authorization": "Bearer caller-token"}
    )

    plain = {"resourceType": "Parameters", "parameter": []}
    assert rebuild_at_external_fhir_base_url(user_client, plain) is user_client

    external = {
        "resourceType": "Parameters",
        "parameter": [{"name": "externalFhirBaseUrl", "valueUri": "http://ehr.example/fhir"}],
    }
    rebuilt = rebuild_at_external_fhir_base_url(user_client, external)
    assert rebuilt.url == "http://ehr.example/fhir"
    assert rebuilt.extra_headers == {"Authorization": "Bearer caller-token"}


async def test_client_that_may_not_read_forms_cannot_extract(fhir_client, safe_db):
    questionnaire = await create_extracting_questionnaire(fhir_client, "refused-patient")

    with pytest.raises(BaseFHIRError):
        await extract_as(fhir_client, "sdc-no-forms", questionnaire)

    written = await fhir_client.resources("Patient").search(_id="refused-patient").fetch_all()
    assert written == []


async def test_client_that_may_read_forms_extracts(fhir_client, safe_db):
    questionnaire = await create_extracting_questionnaire(fhir_client, "extracted-patient")

    await extract_as(fhir_client, "sdc", questionnaire)

    patient = await fhir_client.resources("Patient").search(_id="extracted-patient").get()
    assert patient.id == "extracted-patient"


async def create_extracting_questionnaire(fhir_client, patient_id):
    mapping = fhir_client.resource(
        "Mapping",
        body={
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": [
                {
                    "request": {"method": "PUT", "url": f"Patient/{patient_id}"},
                    "resource": {"resourceType": "Patient", "id": patient_id},
                }
            ],
        },
    )
    await mapping.save()
    return await create_questionnaire(
        fhir_client,
        {"status": "active", "extension": [make_questionnaire_mapper_ext(mapping.id)], "item": []},
    )


async def extract_as(fhir_client, client_id, questionnaire):
    caller = build_seeded_client(fhir_client, client_id)
    return await caller.execute(
        f"Questionnaire/{questionnaire.id}/$extract",
        method="POST",
        data={"resourceType": "QuestionnaireResponse", "questionnaire": questionnaire.id},
    )


async def test_transaction_is_authorized_entry_by_entry(fhir_client, safe_db):
    caller = build_seeded_client(fhir_client, "sdc-no-forms")
    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"method": "PUT", "url": "Organization/not-granted"},
                "resource": {"resourceType": "Organization", "id": "not-granted"},
            }
        ],
    }

    with pytest.raises(BaseFHIRError, match=r"entry\[0\]"):
        await caller.execute("/", data=bundle)

    written = await fhir_client.resources("Organization").search(_id="not-granted").fetch_all()
    assert written == []


def build_seeded_client(fhir_client, client_id):
    """A client with a seeded Client's own credentials; see initBundle.json."""
    token = base64.b64encode(f"{client_id}:{client_id}-secret".encode()).decode()
    return AsyncFHIRClient(fhir_client.url, authorization=f"Basic {token}")
