import pytest

from tests.factories import (
    QUESTIONNAIRE_PROFILE_URL,
    create_address_questionnaire,
    make_parameters,
    create_questionnaire,
    make_launch_context_ext,
    make_questionnaire,
    make_source_queries_ext,
    make_initial_expression_ext,
    make_item_population_context_ext,
    make_variable_ext,
    make_sub_questionnaire_ext,
    make_assembled_from_ext,
)


@pytest.mark.asyncio
async def test_assemble_then_populate(fhir_client, safe_db):
    address = await create_address_questionnaire(fhir_client)

    appointment = await create_questionnaire(
        fhir_client,
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
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_source_queries_ext("#PrePopQuery"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "last-appointment",
                    "extension": [
                        make_initial_expression_ext(
                            "%PrePopQuery.entry.resource.entry.resource.start"
                        )
                    ],
                },
            ],
        },
    )

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_launch_context_ext("LaunchPatient", "Patient")],
            "item": [
                {
                    "linkId": "appointment",
                    "type": "display",
                    "text": "Sub questionnaire is not supported",
                    "extension": [make_sub_questionnaire_ext(appointment.id)],
                },
                {
                    "type": "group",
                    "linkId": "patient-address",
                    "extension": [
                        make_item_population_context_ext("%LaunchPatient.address")
                    ],
                    "item": [
                        {
                            "linkId": "patient-address-display",
                            "type": "display",
                            "text": "Sub questionanire is not supported",
                            "extension": [
                                make_variable_ext("prefix", "'patient-address-'"),
                                make_sub_questionnaire_ext(address.id),
                            ],
                        }
                    ],
                },
                {
                    "type": "group",
                    "linkId": "patient-contact",
                    "repeats": True,
                    "extension": [
                        make_item_population_context_ext("%LaunchPatient.contact")
                    ],
                    "item": [
                        {
                            "type": "group",
                            "linkId": "patient-contanct-address",
                            "extension": [make_item_population_context_ext("address")],
                            "item": [
                                {
                                    "linkId": "patient-contact-address-display",
                                    "type": "display",
                                    "text": "Sub questionanire is not supported",
                                    "extension": [
                                        make_variable_ext(
                                            "prefix", "'patient-contact-address-'"
                                        ),
                                        make_sub_questionnaire_ext(address.id),
                                    ],
                                }
                            ],
                        }
                    ],
                },
            ],
        },
    )

    assembled = await q.execute("$assemble", method="get")

    del assembled["meta"]["lastUpdated"]
    del assembled["meta"]["versionId"]
    del assembled["meta"]["extension"]

    assert assembled == {
        "resourceType": "Questionnaire",
        "meta": {"profile": [QUESTIONNAIRE_PROFILE_URL]},
        "status": "active",
        "extension": [
            make_launch_context_ext("LaunchPatient", "Patient"),
            make_source_queries_ext("#PrePopQuery"),
            make_assembled_from_ext(q.id),
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
                "extension": [
                    make_initial_expression_ext(
                        "%PrePopQuery.entry.resource.entry.resource.start"
                    )
                ],
            },
            {
                "type": "group",
                "linkId": "patient-address",
                "extension": [
                    make_item_population_context_ext("%LaunchPatient.address")
                ],
                "item": [
                    {
                        "linkId": "patient-address-line-1",
                        "type": "string",
                        "extension": [make_initial_expression_ext("line[0]")],
                    },
                    {
                        "linkId": "patient-address-line-2",
                        "type": "string",
                        "extension": [make_initial_expression_ext("line[1]")],
                        "enableWhen": [
                            {
                                "question": "patient-address-line-1",
                                "operator": "exists",
                                "answerBoolean": True,
                            }
                        ],
                    },
                ],
            },
            {
                "type": "group",
                "linkId": "patient-contact",
                "repeats": True,
                "extension": [
                    make_item_population_context_ext("%LaunchPatient.contact")
                ],
                "item": [
                    {
                        "type": "group",
                        "linkId": "patient-contanct-address",
                        "extension": [make_item_population_context_ext("address")],
                        "item": [
                            {
                                "linkId": "patient-contact-address-line-1",
                                "type": "string",
                                "extension": [make_initial_expression_ext("line[0]")],
                            },
                            {
                                "linkId": "patient-contact-address-line-2",
                                "type": "string",
                                "extension": [make_initial_expression_ext("line[1]")],
                                "enableWhen": [
                                    {
                                        "question": "patient-contact-address-line-1",
                                        "operator": "exists",
                                        "answerBoolean": True,
                                    }
                                ],
                            },
                        ],
                    }
                ],
            },
        ],
    }

    patient = fhir_client.resource("Patient")
    await patient.save()

    appointment = fhir_client.resource(
        "Appointment",
        **{
            "status": "booked",
            "start": "2020-01-01T00:00:00Z",
            "end": "2020-01-01T00:00:00Z",
            "participant": [{"status": "accepted", "actor": patient}],
        },
    )
    await appointment.save()

    p = await fhir_client.execute(
        "Questionnaire/$populate",
        data=make_parameters(LaunchPatient=patient, questionnaire=assembled),
    )

    assert p == {
        "item": [
            {
                "answer": [{"valueString": "2020-01-01T00:00:00Z"}],
                "linkId": "last-appointment",
            },
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
