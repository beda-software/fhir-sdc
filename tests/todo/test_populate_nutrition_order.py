import pytest
from fhirpathpy import evaluate as fhirpath

from app.test.utils import create_parameters


@pytest.mark.asyncio
async def test_populate_nutritio_order(fhir_client, safe_db):
    """
    TODO think how this kind of error may be handled
    Shown typo (missing bracket) causes an empty bundle response
    The system should check such cases an fire warnings
    """
    q = fhir_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
                    "extension": [
                        {
                            "url": "name",
                            "valueCoding": {
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                                "code": "LaunchPatient",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
                    "valueReference": {"reference": "#DietAndNutrition"},
                },
            ],
            "contained": [
                {
                    "id": "DietAndNutrition",
                    "type": "batch",
                    "entry": [
                        {
                            "request": {  # -------second bracket is missing here \/
                                "url": "/NutritionOrder?patient={{%LaunchPatient.id}&status=active",
                                "method": "GET",
                            }
                        }
                    ],
                    "resourceType": "Bundle",
                }
            ],
            "item": [
                {
                    "text": "Diet and Nutrition",
                    "type": "choice",
                    "linkId": "diet",
                    "repeats": True,
                    "answerValueSet": "diet",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%DietAndNutrition.entry[0].resource.entry.resource.oralDiet.type.coding.where(system = 'http://snomed.info/sct')",
                            },
                        }
                    ],
                }
            ],
        },
    )
    await q.save()

    assert q.id is not None

    launch_patient = fhir_client.resource("Patient")
    await launch_patient.save()

    assert launch_patient.id is not None

    n = fhir_client.resource(
        "NutritionOrder",
        **{
            "intent": "plan",
            "status": "active",
            "patient": {"id": launch_patient.id, "resourceType": "Patient"},
            "dateTime": "2020-01-01T00:00:00Z",
            "oralDiet": {
                "type": [
                    {
                        "coding": [
                            {
                                "code": "437091000124100",
                                "system": "http://snomed.info/sct",
                                "display": "Calcium modified diet",
                            }
                        ]
                    }
                ]
            },
        },
    )

    await n.save()
    assert n.id is not None
    p = await q.execute(
        "$populate", data=create_parameters(LaunchPatient=launch_patient)
    )

    populated_answer = fhirpath(
        p, "QuestionnaireResponse.item.where(linkId='diet').answer.valueCoding"
    )
    assert populated_answer == []
    # {
    #     "code": "437091000124100",
    #     "system": "http://snomed.info/sct",
    #     "display": "Calcium modified diet",
    # }
