import pytest

from tests.factories import (
    create_questionnaire,
    make_parameters,
    make_launch_context_ext,
    make_questionnaire,
    make_source_queries_ext,
    make_initial_expression_ext,
    make_item_population_context_ext
)

questionnaire = make_questionnaire({
    "id": "example-questionnaire",
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
})

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
async def test_populate_v3(fhir_client, safe_db):
    patient_example = fhir_client.resource("Patient", **env["patient"])

    await patient_example.save()

    assert patient_example.id is not None
    q = await create_questionnaire(
        fhir_client,
        questionnaire
    )
    questionnaire_response = await q.execute("$populate", data=make_parameters(patient=patient_example))

    assert questionnaire_response == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "firstName",
                        "answer": [
                            {"valueString": "Peter"},
                            {"valueString": "Middlename"},
                            {"valueString": "Pit"},
                            {"valueString": "Little Pitty"},
                        ],
                    }
                ],
                "linkId": "names",
            },
        ],
        "questionnaire": questionnaire["id"],
        "resourceType": "QuestionnaireResponse",
    }
