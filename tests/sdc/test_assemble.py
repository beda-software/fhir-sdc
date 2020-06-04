async def create_questionnaire(sdk, questionnaire):
    q = sdk.client.resource("Questionnaire", **questionnaire)
    await q.save()
    assert q.id is not None
    return q


async def test_assemble_sub_questionnaire(sdk, safe_db):
    get_given_name = await create_questionnaire(
        sdk,
        {
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "itemContext": {
                "language": "text/fhirpath",
                "expression": "%LaunchPatient.name",
            },
            "item": [
                {
                    "type": "string",
                    "linkId": "firstName",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "given.first()",
                    },
                },
            ],
        },
    )

    get_family_name = await create_questionnaire(
        sdk,
        {
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "itemContext": {
                "language": "text/fhirpath",
                "expression": "%LaunchPatient.name",
            },
            "item": [
                {
                    "type": "string",
                    "linkId": "familyName",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "family",
                    },
                },
            ],
        },
    )

    q = await create_questionnaire(
        sdk,
        {
            "status": "active",
            "resourceType": "Questionnaire",
            "item": [
                {
                    "linkId": "demographics",
                    "type": "group",
                    "item": [
                        {
                            "type": "display",
                            "linkId": "givenNameGroup",
                            "text": "Sub questionnaire is not supported",
                            "subQuestionnaire": get_given_name.id,
                        },
                        {
                            "type": "display",
                            "linkId": "familyNameGroup",
                            "text": "Sub questionnaire is not supported",
                            "subQuestionnaire": get_family_name.id,
                        },
                    ],
                }
            ],
        },
    )

    assembled = await q.execute("$assemble", method="get")

    del assembled["meta"]

    assert assembled == {
        "assembledFrom": q.id,
        "resourceType": "Questionnaire",
        "status": "active",
        "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
        "item": [
            {
                "linkId": "demographics",
                "type": "group",
                "itemContext": {
                    "language": "text/fhirpath",
                    "expression": "%LaunchPatient.name",
                },
                "item": [
                    {
                        "type": "string",
                        "linkId": "firstName",
                        "initialExpression": {
                            "language": "text/fhirpath",
                            "expression": "given.first()",
                        },
                    },
                    {
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
    }


async def test_assemble_reuse_questionnaire(sdk, safe_db):
    address = await create_questionnaire(
        sdk,
        {
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "assembleContext": [{"name": "prefix", "type": "string"}],
            "item": [
                {
                    "linkId": "{{%prefix}}line-1",
                    "type": "string",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "line[0]",
                    },
                },
                {
                    "linkId": "{{%prefix}}line-2",
                    "type": "string",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "line[1]",
                    },
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

    q = await create_questionnaire(
        sdk,
        {
            "status": "actice",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "item": [
                {
                    "type": "group",
                    "linkId": "patient-address",
                    "itemContext": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.address",
                    },
                    "item": [
                        {
                            "linkId": "patient-address-display",
                            "type": "display",
                            "text": "Sub questionanire is not supported",
                            "varaible": [
                                {
                                    "name": "prefix",
                                    "language": "text/fhirpath",
                                    "expression": "'patient-address-'",
                                }
                            ],
                            "subQuestionnaire": address.id,
                        }
                    ],
                },
                {
                    "type": "group",
                    "linkId": "patient-contact",
                    "repeats": True,
                    "itemContext": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.contact",
                    },
                    "item": [
                        {
                            "type": "group",
                            "linkId": "patient-contanct-address",
                            "itemContext": {
                                "language": "text/fhirpath",
                                "expression": "address",
                            },
                            "item": [
                                {
                                    "linkId": "patient-contact-address-display",
                                    "type": "display",
                                    "text": "Sub questionanire is not supported",
                                    "varaible": [
                                        {
                                            "name": "prefix",
                                            "language": "text/fhirpath",
                                            "expression": "'patient-contact-address-'",
                                        }
                                    ],
                                    "subQuestionnaire": address.id,
                                }
                            ],
                        }
                    ],
                },
            ],
        },
    )

    assembled = await q.execute("$assemble", method="get")

    del assembled["meta"]

    assert assembled == {
        "assembledFrom": q.id,
        "resourceType": "Questionnaire",
        "status": "actice",
        "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
        "item": [
            {
                "type": "group",
                "linkId": "patient-address",
                "itemContext": {
                    "language": "text/fhirpath",
                    "expression": "%LaunchPatient.address",
                },
                "item": [
                    {
                        "linkId": "patient-address-line-1",
                        "type": "string",
                        "initialExpression": {
                            "language": "text/fhirpath",
                            "expression": "line[0]",
                        },
                    },
                    {
                        "linkId": "patient-address-line-2",
                        "type": "string",
                        "initialExpression": {
                            "language": "text/fhirpath",
                            "expression": "line[1]",
                        },
                        "enableWhen": [
                            {
                                "question": "patient-address-line-1",
                                "operator": "exists",
                                "answer": {"boolean": True},
                            }
                        ],
                    },
                ],
            },
            {
                "type": "group",
                "linkId": "patient-contact",
                "repeats": True,
                "itemContext": {
                    "language": "text/fhirpath",
                    "expression": "%LaunchPatient.contact",
                },
                "item": [
                    {
                        "type": "group",
                        "linkId": "patient-contanct-address",
                        "itemContext": {
                            "language": "text/fhirpath",
                            "expression": "address",
                        },
                        "item": [
                            {
                                "linkId": "patient-contact-address-line-1",
                                "type": "string",
                                "initialExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "line[0]",
                                },
                            },
                            {
                                "linkId": "patient-contact-address-line-2",
                                "type": "string",
                                "initialExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "line[1]",
                                },
                                "enableWhen": [
                                    {
                                        "question": "patient-contact-address-line-1",
                                        "operator": "exists",
                                        "answer": {"boolean": True},
                                    }
                                ],
                            },
                        ],
                    }
                ],
            },
        ],
    }
