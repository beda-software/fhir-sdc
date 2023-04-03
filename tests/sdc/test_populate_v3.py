from app.operations.populate import populate

questionnaire = {
    "resourceType": "Questionnaire",
    "id": "example-questionnaire",
    "status": "active",
    "launchContext": [
        {
            "name": {
                "code": "patient"
            },
            "type": ["Patient"],
            "description": "Patient resource"
        }
    ],
    "contained": [
        {
            "resourceType": "Bundle",
            "id": "Example",
            "type": "transaction",
            "entry": [
                {
                  "request": {
                      "method": "GET",
                      "url": "/Patient"
                  }
                }
            ]
        }
    ],
    "sourceQueries": {
        "localRef": "Bundle#Example"
    },
    "item": [
        {
            "type": "group",
            "linkId": "example",
            "item": [
                {
                    "text": "example",
                    "type": "string",
                    "linkId": "example",
                    "hidden": True,
                    "itemPopulationContext": {
                      "language": "text/fhirpath",
                      "expression": "%Expression"
                    },
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "name.given.first()"
                    }
                }
            ]
        }
    ],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"]
    },
}

env = {'patient': {'resourceType': 'Patient', 'id': 'example-patient', 'name': [{'given': ['Name'], 'family': 'Name'}]}}


async def test_populate_v3(sdk, safe_db):
    qr = await populate(sdk.client, questionnaire, env)

    assert qr == {'item': [{'item': [{'linkId': 'example',
                            'text': 'example'}],
                            'linkId': 'example'}],
                  'questionnaire': 'example-questionnaire',
                  'resourceType': 'QuestionnaireResponse',
                  }
