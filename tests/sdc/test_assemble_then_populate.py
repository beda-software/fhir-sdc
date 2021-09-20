from tests.utils import create_parameters


async def create_questionnaire(sdk, questionnaire):
    q = sdk.client.resource("Questionnaire", **questionnaire)
    await q.save()
    assert q.id is not None
    return q

async def create_address_questionnaire(sdk):
    return await create_questionnaire(
        sdk,
        {
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "assembleContext": [{"name": "prefix", "type": "string"}],
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


async def test_assemble_then_populate(sdk, safe_db):
    address = await create_address_questionnaire(sdk)

    appointment = await create_questionnaire(
        sdk,
        {
            "status": "active",
            "contained": [
                {
                    "resourceType": "Bundle",
                    "id": "PrePopQuery",
                    "type": "batch",
                    "entry": [
                        {
                            "request": {
                                "method": "GET",
                                "url": "Appointment?patient={{%LaunchPatient.id}}",
                            },
                        },
                    ],
                }
            ],
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "sourceQueries": [{"localRef": "Bundle#PrePopQuery"}],
            "item": [
                {
                    "type": "string",
                    "linkId": "last-appointment",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%PrePopQuery.entry.resource.entry.resource.start",
                    },
                },
            ],
        },
    )

    q = await create_questionnaire(
        sdk,
        {
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "item": [
                {
                    "linkId": "patient-appointment-display",
                    "type": "display",
                    "text": "Sub questionanire is not supported",
                    "subQuestionnaire": appointment.id,
                },
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
                            "variable": [
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
                            "itemContext": {"language": "text/fhirpath", "expression": "address"},
                            "item": [
                                {
                                    "linkId": "patient-contact-address-display",
                                    "type": "display",
                                    "text": "Sub questionanire is not supported",
                                    "variable": [
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
        "status": "active",
        "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
        "sourceQueries": [{"localRef": "Bundle#PrePopQuery"}],
        "contained": [
            {
                "resourceType": "Bundle",
                "id": "PrePopQuery",
                "type": "batch",
                "entry": [
                    {
                        "request": {
                            "method": "GET",
                            "url": "Appointment?patient={{%LaunchPatient.id}}",
                        },
                    },
                ],
            }
        ],
        "item": [
            {
                "type": "string",
                "linkId": "last-appointment",
                "initialExpression": {
                    "language": "text/fhirpath",
                    "expression": "%PrePopQuery.entry.resource.entry.resource.start",
                },
            },
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
                        "itemContext": {"language": "text/fhirpath", "expression": "address"},
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

    patient = sdk.client.resource("Patient")
    await patient.save()

    appointment = sdk.client.resource(
        "Appointment",
        **{
            "status": "booked",
            "start": "2020-01-01T00:00",
            "participant": [{"status": "accepted", "actor": patient}],
        },
    )
    await appointment.save()

    p = await sdk.client.execute(
        "Questionnaire/$populate",
        data=create_parameters(LaunchPatient=patient, questionnaire=assembled),
    )

    assert p == {
        "item": [
            {"answer": [{"value": {"string": "2020-01-01T00:00"}}], "linkId": "last-appointment"},
            {
                "item": [
                    {"linkId": "patient-address-line-1"},
                    {"linkId": "patient-address-line-2"},
                ],
                "linkId": "patient-address",
            },
        ],
        "questionnaire": None,
        "resourceType": "QuestionnaireResponse",
    }
