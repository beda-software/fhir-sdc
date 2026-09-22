import pytest
from faker import Faker
from fhirpathpy import evaluate as fhirpath

from app.aidbox.utils import get_organization_client
from tests.factories import (
    make_initial_expression_ext,
    make_item_population_context_ext,
    make_launch_context_ext,
    make_parameters,
    make_questionnaire,
    make_questionnaire_mapper_ext,
    make_source_queries_ext,
)

fake = Faker()


async def get_questionnaire():
    return make_questionnaire(
        {
            "resourceType": "Questionnaire",
            "status": "active",
            "extension": [
                make_launch_context_ext("patient", "Patient"),
                make_source_queries_ext("#PrePopQuery"),
            ],
            "contained": [
                {
                    "resourceType": "Bundle",
                    "id": "PrePopQuery",
                    "type": "batch",
                    "entry": [
                        {
                            "request": {
                                "method": "GET",
                                "url": "Patient?_id={{%patient.id}}",
                            },
                        },
                    ],
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                    "extension": [make_initial_expression_ext("%patient.id")],
                },
                {
                    "type": "group",
                    "linkId": "names",
                    "extension": [
                        make_item_population_context_ext(
                            "%PrePopQuery.entry.resource.entry.resource.name"
                        )
                    ],
                    "item": [
                        {
                            "repeats": True,
                            "type": "string",
                            "linkId": "firstName",
                            "extension": [make_initial_expression_ext("given")],
                        },
                    ],
                },
            ],
        }
    )


@pytest.mark.asyncio
async def test_organization_client(aidbox_client, safe_db):
    org_1 = aidbox_client.resource("Organization", **{"name": "org_1"})
    await org_1.save()
    org_2 = aidbox_client.resource("Organization", **{"name": "org_2"})
    await org_2.save()

    org_1_client = get_organization_client(aidbox_client, org_1)
    org_2_client = get_organization_client(aidbox_client, org_2)

    patient1 = org_1_client.resource("Patient")
    await patient1.save()

    assert len(await org_2_client.resources("Patient").search(_id=patient1.id).fetch_all()) == 0


@pytest.mark.asyncio
async def test_populate(aidbox_client, safe_db):
    given = fake.first_name()

    org_1 = aidbox_client.resource("Organization", **{"name": "org_1"})
    await org_1.save()
    org_1_client = get_organization_client(aidbox_client, org_1)

    questionnaire = await get_questionnaire()
    q = org_1_client.resource("Questionnaire", **questionnaire)
    await q.save()

    patient1 = org_1_client.resource("Patient", name=[{"given": [given]}])
    await patient1.save()

    launch_patient = {"resourceType": "Patient", "id": patient1.id}

    p = await q.execute("$populate", data=make_parameters(patient=launch_patient))

    assert fhirpath(
        p,
        "QuestionnaireResponse.repeat(item).where(linkId='firstName').answer.valueString",
        {},
    ) == [given]


async def create_org_questionnaire(aidbox_client, name, patient_id):
    org = aidbox_client.resource("Organization", **{"name": name})
    await org.save()
    org_client = get_organization_client(aidbox_client, org)

    mapping = org_client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"method": "PUT", "url": f"Patient/{patient_id}"},
                        "resource": {"resourceType": "Patient", "id": patient_id},
                    }
                ],
            }
        },
    )
    await mapping.save()
    q = org_client.resource(
        "Questionnaire",
        **make_questionnaire(
            {
                "status": "active",
                "extension": [make_questionnaire_mapper_ext(mapping.id)],
                "item": [],
            }
        ),
    )
    await q.save()
    return org_client, q


@pytest.mark.asyncio
async def test_extract_instance_endpoint(aidbox_client, safe_db):
    org_client, q = await create_org_questionnaire(aidbox_client, "org_i", "extracted-instance")

    extraction = await q.execute(
        "$extract", data=org_client.resource("QuestionnaireResponse", questionnaire=q.id)
    )
    assert len(extraction) == 1

    patient = await org_client.resources("Patient").search(_id="extracted-instance").get()
    assert patient.id == "extracted-instance"


@pytest.mark.asyncio
async def test_extract_collection_endpoint(aidbox_client, safe_db):
    org_client, q = await create_org_questionnaire(aidbox_client, "org_c", "extracted-collection")

    extraction = await org_client.execute(
        "Questionnaire/$extract",
        method="POST",
        data={"resourceType": "QuestionnaireResponse", "questionnaire": q.id},
        params=None,
    )
    assert len(extraction) == 1

    patient = await org_client.resources("Patient").search(_id="extracted-collection").get()
    assert patient.id == "extracted-collection"
