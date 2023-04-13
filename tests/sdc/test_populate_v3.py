import pytest

from app.sdc.populate import populate

questionnaire = {
    "resourceType": "Questionnaire",
    "id": "example-questionnaire",
    "status": "active",
    "launchContext": [
        {
            "name": {"code": "patient"},
            "type": ["Patient"],
        },
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
    "sourceQueries": [{"localRef": "Bundle#PrePopQuery"}],
    "item": [
        {
            "type": "group",
            "linkId": "names",
            "itemPopulationContext": {
                "language": "text/fhirpath",
                "expression": "%PrePopQuery.entry.resource.entry.resource.name",
            },
            "item": [
                {
                    "repeats": True,
                    "type": "string",
                    "linkId": "firstName",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "given",
                    },
                },
            ],
        },
    ],
}

env = {
    "patient": {
        "id": "example",
        "resourceType": "Patient",
        "name": [
            {"given": ["Peter", "Middlename"]},
            {"given": ["Pit"]},
            {"given": ["Little Pitty"]},
        ],
    }
}


@pytest.mark.asyncio
async def test_populate_v3(aidbox_client, safe_db):
    patient_example = aidbox_client.resource("Patient", **env["patient"])

    await patient_example.save()

    assert patient_example.id is not None

    questionnaire_response = await populate(aidbox_client, questionnaire, env)

    assert questionnaire_response == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "firstName",
                        "answer": [
                            {"value": {"string": "Peter"}},
                            {"value": {"string": "Middlename"}},
                            {"value": {"string": "Pit"}},
                            {"value": {"string": "Little Pitty"}},
                        ],
                    }
                ],
                "linkId": "names",
            },
        ],
        "questionnaire": questionnaire["id"],
        "resourceType": "QuestionnaireResponse",
    }
