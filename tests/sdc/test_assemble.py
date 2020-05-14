async def create_questionnaire(sdk, questionnaire):
    q = sdk.client.resource("Questionnaire", **questionnaire)
    await q.save()
    assert q.id is not None
    return q


async def test_assemble_standalone(sdk, safe_db):
    get_given_name = await create_questionnaire(
        sdk,
        {
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient",},],
            "item": [
                {
                    "type": "group",
                    "linkId": "names",
                    "itemContext": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name",
                    },
                    "item": [
                        {
                            "repeats": True,
                            "type": "string",
                            "linkId": "firstName",
                            "initialExpression": {
                                "language": "text/fhirpath",
                                "expression": "given.first()",
                            },
                        },
                    ],
                },
            ],
        },
    )

    get_family_name = await create_questionnaire(
        sdk,
        {
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient",},],
            "item": [
                {
                    "type": "group",
                    "linkId": "names",
                    "itemContext": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name",
                    },
                    "item": [
                        {
                            "repeats": True,
                            "type": "string",
                            "linkId": "familyName",
                            "initialExpression": {
                                "language": "text/fhirpath",
                                "expression": "family",
                            },
                        },
                    ],
                },
            ],
        },
    )

    q = await create_questionnaire(
        sdk,
        {
            "status": "actice",
            "item": [
                {
                    "type": "group",
                    "linkId": "givenNameGroup",
                    "subQuestionnaire": get_given_name.id,
                },
                {
                    "type": "group",
                    "linkId": "familyNameGroup",
                    "subQuestionnaire": get_family_name.id,
                },
            ],
        },
    )

    assembled = await q.execute("$assemble", method="get")

    del assembled["meta"]

    assert assembled == {
        "id": q.id,
        "resourceType": "Questionnaire",
        "status": "actice",
        "item": [
            {
                "type": "group",
                "linkId": "givenNameGroup",
                "item": [
                    {
                        "type": "group",
                        "linkId": "names",
                        "itemContext": {
                            "language": "text/fhirpath",
                            "expression": "%LaunchPatient.name",
                        },
                        "item": [
                            {
                                "repeats": True,
                                "type": "string",
                                "linkId": "firstName",
                                "initialExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "given.first()",
                                },
                            },
                        ],
                    }
                ],
            },
            {
                "type": "group",
                "linkId": "familyNameGroup",
                "item": [
                    {
                        "type": "group",
                        "linkId": "names",
                        "itemContext": {
                            "language": "text/fhirpath",
                            "expression": "%LaunchPatient.name",
                        },
                        "item": [
                            {
                                "repeats": True,
                                "type": "string",
                                "linkId": "familyName",
                                "initialExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "family",
                                },
                            },
                        ],
                    }
                ],
            },
        ],
    }


async def test_assemble_embed(sdk, safe_db):
    pass
