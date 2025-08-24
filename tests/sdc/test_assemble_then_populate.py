import pytest

from app.test.utils import (
    create_address_questionnaire,
    create_parameters,
    create_questionnaire,
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
                    "valueReference": {"reference": "#PrePopQuery"},
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "last-appointment",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%PrePopQuery.entry.resource.entry.resource.start",
                            },
                        }
                    ],
                },
            ],
        },
    )

    q = await create_questionnaire(
        fhir_client,
        {
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
                }
            ],
            "item": [
                {
                    "linkId": "appointment",
                    "type": "display",
                    "text": "Sub questionnaire is not supported",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                            "valueCanonical": appointment.id,
                        }
                    ],
                },
                {
                    "type": "group",
                    "linkId": "patient-address",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%LaunchPatient.address",
                            },
                        }
                    ],
                    "item": [
                        {
                            "linkId": "patient-address-display",
                            "type": "display",
                            "text": "Sub questionanire is not supported",
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/StructureDefinition/variable",
                                    "valueExpression": {
                                        "name": "prefix",
                                        "language": "text/fhirpath",
                                        "expression": "'patient-address-'",
                                    },
                                },
                                {
                                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                                    "valueCanonical": address.id,
                                },
                            ],
                        }
                    ],
                },
                {
                    "type": "group",
                    "linkId": "patient-contact",
                    "repeats": True,
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%LaunchPatient.contact",
                            },
                        }
                    ],
                    "item": [
                        {
                            "type": "group",
                            "linkId": "patient-contanct-address",
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                                    "valueExpression": {
                                        "language": "text/fhirpath",
                                        "expression": "address",
                                    },
                                }
                            ],
                            "item": [
                                {
                                    "linkId": "patient-contact-address-display",
                                    "type": "display",
                                    "text": "Sub questionanire is not supported",
                                    "extension": [
                                        {
                                            "url": "http://hl7.org/fhir/StructureDefinition/variable",
                                            "valueExpression": {
                                                "name": "prefix",
                                                "language": "text/fhirpath",
                                                "expression": "'patient-contact-address-'",
                                            },
                                        },
                                        {
                                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                                            "valueCanonical": address.id,
                                        },
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

    del assembled["meta"]

    assert assembled == {
        "resourceType": "Questionnaire",
        "status": "active",
        "extension": [
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
                "extension": [
                    {
                        "url": "name",
                        "valueCoding": {
                            "code": "LaunchPatient",
                            "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        },
                    },
                    {"url": "type", "valueCode": "Patient"},
                ],
            },
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
                "valueReference": {"reference": "#PrePopQuery"},
            },
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembledFrom",
                "valueCanonical": q.id,
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
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%PrePopQuery.entry.resource.entry.resource.start",
                        },
                    }
                ],
            },
            {
                "type": "group",
                "linkId": "patient-address",
                "extension": [
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%LaunchPatient.address",
                        },
                    }
                ],
                "item": [
                    {
                        "linkId": "patient-address-line-1",
                        "type": "string",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "line[0]",
                                },
                            }
                        ],
                    },
                    {
                        "linkId": "patient-address-line-2",
                        "type": "string",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "line[1]",
                                },
                            }
                        ],
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
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%LaunchPatient.contact",
                        },
                    }
                ],
                "item": [
                    {
                        "type": "group",
                        "linkId": "patient-contanct-address",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "address",
                                },
                            }
                        ],
                        "item": [
                            {
                                "linkId": "patient-contact-address-line-1",
                                "type": "string",
                                "extension": [
                                    {
                                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                        "valueExpression": {
                                            "language": "text/fhirpath",
                                            "expression": "line[0]",
                                        },
                                    }
                                ],
                            },
                            {
                                "linkId": "patient-contact-address-line-2",
                                "type": "string",
                                "extension": [
                                    {
                                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                        "valueExpression": {
                                            "language": "text/fhirpath",
                                            "expression": "line[1]",
                                        },
                                    }
                                ],
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
            "participant": [{"status": "accepted", "actor": patient}],
        },
    )
    await appointment.save()

    p = await fhir_client.execute(
        "Questionnaire/$populate",
        data=create_parameters(LaunchPatient=patient, questionnaire=assembled),
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
