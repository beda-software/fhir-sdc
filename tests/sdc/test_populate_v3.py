import pytest

from app.test.utils import create_parameters

questionnaire = {
    "resourceType": "Questionnaire",
    "id": "example-questionnaire",
    "status": "active",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "patient",
                    },
                },
                {"url": "type", "valueCode": "Patient"},
            ],
        },
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
            "valueReference": {"reference": "#PrePopQuery"},
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
    "item": [
        {
            "type": "group",
            "linkId": "names",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%PrePopQuery.entry.resource.entry.resource.name",
                    },
                }
            ],
            "item": [
                {
                    "repeats": True,
                    "type": "string",
                    "linkId": "firstName",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "given",
                            },
                        }
                    ],
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
async def test_populate_v3(fhir_client, safe_db):
    patient_example = fhir_client.resource("Patient", **env["patient"])

    await patient_example.save()

    assert patient_example.id is not None
    q = fhir_client.resource(
        "Questionnaire", **questionnaire
    )
    await q.save()
    questionnaire_response = await q.execute("$populate", data=create_parameters(patient=patient_example))

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
