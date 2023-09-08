def create_parameters(**payload):
    return {
        "resourceType": "Parameters",
        "parameter": [{"name": name, "resource": resource} for name, resource in payload.items()],
    }


async def create_questionnaire(aidbox_client, questionnaire):
    q = aidbox_client.resource("Questionnaire", **questionnaire)
    await q.save()
    assert q.id is not None
    return q


async def create_address_questionnaire(aidbox_client):
    return await create_questionnaire(
        aidbox_client,
        {
            "status": "active",
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
            "assembleContext": "prefix",
            "item": [
                {
                    "linkId": "{{%prefix}}line-1",
                    "type": "string",
                    "initialExpression": {"language": "text/fhirpath", "expression": "line[0]"},
                },
                {
                    "linkId": "{{%prefix}}line-2",
                    "type": "string",
                    "initialExpression": {"language": "text/fhirpath", "expression": "line[1]"},
                    "enableWhen": [
                        {
                            "question": "{{%prefix}}line-1",
                            "operator": "exists",
                            "answer": {"boolean": True},
                        }
                    ],
                },
            ],
        },
    )
