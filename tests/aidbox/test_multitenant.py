import pytest
from faker import Faker
from fhirpathpy import evaluate as fhirpath

from app.aidbox.utils import get_organization_client
from app.test.utils import create_parameters
from tests.test_utils import (
    make_launch_context_ext,
    make_source_queries_ext,
    make_item_population_context_ext,
    make_initial_expression_ext
)

fake = Faker()


async def get_questionnaire():
    return {
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
                "extension": [
                    make_initial_expression_ext("%patient.id")
                ],
            },
            {
                "type": "group",
                "linkId": "names",
                "extension": [
                    make_item_population_context_ext("%PrePopQuery.entry.resource.entry.resource.name")
                ],
                "item": [
                    {
                        "repeats": True,
                        "type": "string",
                        "linkId": "firstName",
                        "extension": [
                            make_initial_expression_ext("given")
                        ],
                    },
                ],
            },
        ],
    }


@pytest.mark.asyncio
async def test_organization_client(aidbox_client, safe_db):
    org_1 = aidbox_client.resource("Organization")
    await org_1.save()
    org_2 = aidbox_client.resource("Organization")
    await org_2.save()

    org_1_client = get_organization_client(aidbox_client, org_1)
    org_2_client = get_organization_client(aidbox_client, org_2)

    patient1 = org_1_client.resource("Patient")
    await patient1.save()

    assert (
        len(await org_2_client.resources("Patient").search(_id=patient1.id).fetch_all())
        == 0
    )


@pytest.mark.asyncio
async def test_populate(aidbox_client, safe_db):
    given = fake.first_name()

    org_1 = aidbox_client.resource("Organization")
    await org_1.save()
    org_1_client = get_organization_client(aidbox_client, org_1)

    questionnaire = await get_questionnaire()
    q = org_1_client.resource("Questionnaire", **questionnaire)
    await q.save()

    patient1 = org_1_client.resource("Patient", name=[{"given": [given]}])
    await patient1.save()

    launch_patient = {"resourceType": "Patient", "id": patient1.id}

    p = await q.execute("$populate", data=create_parameters(patient=launch_patient))

    assert fhirpath(
        p,
        "QuestionnaireResponse.repeat(item).where(linkId='firstName').answer.valueString",
        {},
    ) == [given]
