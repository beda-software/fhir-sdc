import pytest
from fhirpy.base.exceptions import OperationOutcome

from app.test.utils import create_address_questionnaire, create_questionnaire


@pytest.mark.asyncio
async def test_assemble_sub_questionnaire(fhir_client, safe_db):
    get_given_name = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name",
                    },
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "firstName",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "given.first()",
                            },
                        }
                    ],
                },
            ],
        },
    )

    get_family_name = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name",
                    },
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "familyName",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "family",
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
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                                    "valueCanonical": get_given_name.id,
                                }
                            ],
                        },
                        {
                            "type": "display",
                            "linkId": "familyNameGroup",
                            "text": "Sub questionnaire is not supported",
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                                    "valueCanonical": get_family_name.id,
                                }
                            ],
                        },
                    ],
                }
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
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembledFrom",
                "valueCanonical": q.id,
            },
        ],
        "item": [
            {
                "linkId": "demographics",
                "type": "group",
                "extension": [
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%LaunchPatient.name",
                        },
                    }
                ],
                "item": [
                    {
                        "type": "string",
                        "linkId": "firstName",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "given.first()",
                                },
                            }
                        ],
                    },
                    {
                        "type": "string",
                        "linkId": "familyName",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "family",
                                },
                            }
                        ],
                    },
                ],
            }
        ],
    }


@pytest.mark.asyncio
async def test_assemble_double_nested_sub_questionnaire(fhir_client, safe_db):
    get_family_name = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name",
                    },
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "familyName",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "family",
                            },
                        }
                    ],
                },
            ],
        },
    )

    get_given_name = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name",
                    },
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "firstName",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "given.first()",
                            },
                        }
                    ],
                },
                {
                    "type": "display",
                    "linkId": "familyNameGroup",
                    "text": "Sub questionnaire is not supported",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                            "valueCanonical": get_family_name.id,
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
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                                    "valueCanonical": get_given_name.id,
                                }
                            ],
                        },
                    ],
                }
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
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembledFrom",
                "valueCanonical": q.id,
            },
        ],
        "item": [
            {
                "linkId": "demographics",
                "type": "group",
                "extension": [
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%LaunchPatient.name",
                        },
                    }
                ],
                "item": [
                    {
                        "type": "string",
                        "linkId": "firstName",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "given.first()",
                                },
                            }
                        ],
                    },
                    {
                        "type": "string",
                        "linkId": "familyName",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "family",
                                },
                            }
                        ],
                    },
                ],
            }
        ],
    }


@pytest.mark.asyncio
async def test_assemble_reuse_questionnaire(fhir_client, safe_db):
    address = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembleContext",
                    "valueString": "prefix",
                },
            ],
            "item": [
                {
                    "linkId": "{{%prefix}}line-1",
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
                    "linkId": "{{%prefix}}line-2",
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
                            "question": "{{%prefix}}line-1",
                            "operator": "exists",
                            "answerBoolean": True,
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                }
            ],
            "item": [
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
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembledFrom",
                "valueCanonical": q.id,
            },
        ],
        "item": [
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


@pytest.mark.asyncio
async def test_validate_assemble_context(fhir_client):
    address = await create_address_questionnaire(fhir_client)

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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                }
            ],
            "item": [
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
                                        "name": "prefix-not-in-assemble-context",
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
                }
            ],
        },
    )
    with pytest.raises(OperationOutcome):
        await q.execute("$assemble", method="get")


@pytest.mark.asyncio
async def test_fhir_assemble_sub_questionnaire(fhir_client, safe_db):
    get_given_name = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                    "valueCanonical": "StructureMap/create-patient",
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name",
                    },
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "firstName",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "given.first()",
                            },
                        }
                    ],
                },
            ],
        },
    )

    get_family_name = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                    "valueCanonical": "StructureMap/create-patient",
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name",
                    },
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "familyName",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "family",
                            },
                        }
                    ],
                },
            ],
        },
    )

    get_line2_address = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                    "valueCanonical": "StructureMap/create-patient",
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "address-line-2",
                },
            ],
        },
    )

    get_address = await create_questionnaire(
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
                                "code": "LaunchPatient",
                                "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            },
                        },
                        {"url": "type", "valueCode": "Patient"},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                    "valueCanonical": "StructureMap/create-patient",
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "line-1",
                },
                {
                    "type": "display",
                    "linkId": "sub-questionnaire-address-line-2",
                    "text": "Sub questionnaire is not supported",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                            "valueCanonical": get_line2_address.id,
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
            "resourceType": "Questionnaire",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                    "valueCanonical": "StructureMap/create-another-patient",
                }
            ],
            "item": [
                {
                    "linkId": "demographics",
                    "type": "group",
                    "item": [
                        {
                            "type": "display",
                            "linkId": "givenNameGroup",
                            "text": "Sub questionnaire is not supported",
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                                    "valueCanonical": get_given_name.id,
                                }
                            ],
                        },
                        {
                            "type": "display",
                            "linkId": "familyNameGroup",
                            "text": "Sub questionnaire is not supported",
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                                    "valueCanonical": get_family_name.id,
                                }
                            ],
                        },
                        {
                            "type": "display",
                            "linkId": "address",
                            "text": "Sub questionnaire",
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
                                    "valueCanonical": get_address.id,
                                }
                            ],
                        },
                    ],
                }
            ],
        },
    )

    assembled = await fhir_client.execute(
        f"Questionnaire/{q['id']}/$assemble", method="get"
    )

    del assembled["meta"]

    assert assembled == {
        "item": [
            {
                "item": [
                    {
                        "type": "string",
                        "linkId": "firstName",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "given.first()",
                                },
                            }
                        ],
                    },
                    {
                        "type": "string",
                        "linkId": "familyName",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                                "valueExpression": {
                                    "language": "text/fhirpath",
                                    "expression": "family",
                                },
                            }
                        ],
                    },
                    {"type": "string", "linkId": "line-1"},
                    {"type": "string", "linkId": "address-line-2"},
                ],
                "type": "group",
                "linkId": "demographics",
                "extension": [
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%LaunchPatient.name",
                        },
                    }
                ],
            }
        ],
        "status": "active",
        "resourceType": "Questionnaire",
        "extension": [
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                "valueCanonical": "StructureMap/create-another-patient",
            },
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                "valueCanonical": "StructureMap/create-patient",
            },
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
                    {
                        "url": "type",
                        "valueCode": "Patient",
                    },
                ],
            },
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembledFrom",
                "valueCanonical": q["id"],
            },
        ],
    }
