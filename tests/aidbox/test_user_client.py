import base64

import pytest
from fhirpy import AsyncFHIRClient
from fhirpy.base.exceptions import BaseFHIRError

from app.sdc.utils import rebuild_at_external_fhir_base_url
from tests.factories import (
    create_questionnaire,
    make_questionnaire_mapper_ext,
    make_sub_questionnaire_ext,
)


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


async def test_client_granted_the_form_reads_runs_every_operation(fhir_client, safe_db):
    assembling, extracting = await create_forms(fhir_client, "extracted-patient")
    caller = build_seeded_client(fhir_client, "sdc")

    assembled = await assemble_as(caller, assembling)
    assert [item["linkId"] for item in assembled["item"][0]["item"]] == ["from-sub-questionnaire"]

    populated = await populate_instance_as(caller, extracting)
    assert populated["resourceType"] == "QuestionnaireResponse"

    populated = await populate_as(caller, extracting)
    assert populated["resourceType"] == "QuestionnaireResponse"

    checked = await constraint_check_as(caller, extracting)
    assert checked["resourceType"] == "QuestionnaireResponse"

    assert len(await extract_instance_as(caller, extracting)) == 1

    assert len(await extract_as(caller, extracting)) == 1
    patient = await fhir_client.resources("Patient").search(_id="extracted-patient").get()
    assert patient.id == "extracted-patient"


async def test_client_without_the_form_reads_is_refused_wherever_forms_are_read(
    fhir_client, safe_db
):
    """Collection $populate and $constraint-check get the Questionnaire inline and read no forms."""
    assembling, extracting = await create_forms(fhir_client, "refused-patient")
    caller = build_seeded_client(fhir_client, "sdc-no-forms")

    with pytest.raises(BaseFHIRError):
        await assemble_as(caller, assembling)

    with pytest.raises(BaseFHIRError):
        await populate_instance_as(caller, extracting)

    with pytest.raises(BaseFHIRError):
        await extract_instance_as(caller, extracting)

    with pytest.raises(BaseFHIRError):
        await extract_as(caller, extracting)

    written = await fhir_client.resources("Patient").search(_id="refused-patient").fetch_all()
    assert written == []


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


async def create_forms(fhir_client, patient_id):
    """A Questionnaire assembled from a sub-Questionnaire, and one extracted by a Mapping."""
    sub_questionnaire = await create_questionnaire(
        fhir_client,
        {"status": "active", "item": [{"type": "string", "linkId": "from-sub-questionnaire"}]},
    )
    assembling = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "linkId": "group",
                    "type": "group",
                    "item": [
                        {
                            "type": "display",
                            "linkId": "sub-questionnaire",
                            "extension": [make_sub_questionnaire_ext(sub_questionnaire.id)],
                        }
                    ],
                }
            ],
        },
    )

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
    extracting = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "url": f"http://example.com/Questionnaire/{patient_id}",
            "extension": [make_questionnaire_mapper_ext(mapping.id)],
            "item": [{"type": "string", "linkId": "note"}],
        },
    )
    return assembling, extracting


def build_seeded_client(fhir_client, client_id):
    """A client with a seeded Client's own credentials; see initBundle.json."""
    token = base64.b64encode(f"{client_id}:{client_id}-secret".encode()).decode()
    return AsyncFHIRClient(fhir_client.url, authorization=f"Basic {token}")


async def assemble_as(caller, questionnaire):
    return await caller.execute(f"Questionnaire/{questionnaire.id}/$assemble", method="GET")


async def extract_as(caller, questionnaire):
    """Name the Questionnaire by canonical url, so fhir-sdc has to search for it by url."""
    return await caller.execute(
        "Questionnaire/$extract",
        method="POST",
        data={"resourceType": "QuestionnaireResponse", "questionnaire": questionnaire["url"]},
    )


async def populate_instance_as(caller, questionnaire):
    return await caller.execute(
        f"Questionnaire/{questionnaire.id}/$populate",
        method="POST",
        data={"resourceType": "Parameters", "parameter": []},
    )


async def populate_as(caller, questionnaire):
    return await caller.execute(
        "Questionnaire/$populate",
        method="POST",
        data={
            "resourceType": "Parameters",
            "parameter": [{"name": "Questionnaire", "resource": questionnaire.serialize()}],
        },
    )


async def constraint_check_as(caller, questionnaire):
    return await caller.execute(
        "QuestionnaireResponse/$constraint-check",
        method="POST",
        data={
            "resourceType": "Parameters",
            "parameter": [
                {"name": "Questionnaire", "resource": questionnaire.serialize()},
                {
                    "name": "QuestionnaireResponse",
                    "resource": {"resourceType": "QuestionnaireResponse", "status": "completed"},
                },
            ],
        },
    )


async def extract_instance_as(caller, questionnaire):
    return await caller.execute(
        f"Questionnaire/{questionnaire.id}/$extract",
        method="POST",
        data={"resourceType": "QuestionnaireResponse", "questionnaire": questionnaire.id},
    )
