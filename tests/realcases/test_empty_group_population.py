import utils

questionnaire_data = {
    "resourceType": "Questionnaire",
    "status": "active",
    "launchContext": [
        {
            "name": "LaunchPatient",
            "type": "Patient",
            "description": "The patient that is to be used to pre-populate the form",
        },
        {
            "name": "questionnaire",
            "type": "Questionnaire",
            "description": "This questionnaire template instantiation",
        },
        {
            "name": "RelatedResources",
            "type": "Bundle",
            "description": "Patient's related resources",
        },
    ],
    "contained": [
        {
            "resourceType": "Bundle",
            "id": "RelatedResources",
            "type": "batch",
            "entry": [
                {
                    "request": {
                        "method": "GET",
                        "url": "/MedicationStatement?patient={{%LaunchPatient.id}}&status=active",
                    }
                },
            ],
        }
    ],
    "sourceQueries": [{"localRef": "Bundle#RelatedResources"}],
    "item": [
        {
            "linkId": "group",
            "type": "group",
            "repeats": True,
            "itemContext": {
                "language": "text/fhirpath",
                "expression": "%RelatedResources.entry[0].resource.entry.resource.medication.coding",
            },
            "item": [
                {
                    "linkId": "top-question",
                    "type": "choice",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "where(system = 'http://snomed.info/sct')",
                    },
                    "required": True,
                    "text": "What medicines do you take?",
                    "answerValueSet": "medication",
                },
            ],
        }
    ],
    "id": "generated",
}


async def test_populate(sdk, safe_db):
    p = sdk.client.resource("Patient")
    await p.save()

    questionnaire = sdk.client.resource("Questionnaire", **questionnaire_data)

    p = await sdk.client.execute(
        "Questionnaire/$populate",
        data=utils.create_parameters(LaunchPatient=p, questionnaire=questionnaire),
    )

    assert p == {
        "questionnaire": "generated",
        "resourceType": "QuestionnaireResponse",
    }
