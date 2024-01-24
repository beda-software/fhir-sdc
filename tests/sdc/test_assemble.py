import pytest
from fhirpy.base.exceptions import OperationOutcome

from app.test.utils import create_address_questionnaire, create_questionnaire


@pytest.mark.asyncio
async def test_assemble_sub_questionnaire(aidbox_client, safe_db):
    get_given_name = await create_questionnaire(
        aidbox_client,
        {
            "status": "active",
            "launchContext": [
                {
                    "name": {
                        "code": "LaunchPatient",
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                    },
                    "type": ["Patient"],
                }
            ],
            "itemPopulationContext": {
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
        aidbox_client,
        {
            "status": "active",
            "launchContext": [
                {
                    "name": {
                        "code": "LaunchPatient",
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                    },
                    "type": ["Patient"],
                }
            ],
            "itemPopulationContext": {
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
        aidbox_client,
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
        "launchContext": [
            {
                "name": {
                    "code": "LaunchPatient",
                    "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                },
                "type": ["Patient"],
            }
        ],
        "item": [
            {
                "linkId": "demographics",
                "type": "group",
                "itemPopulationContext": {
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


@pytest.mark.asyncio
async def test_assemble_reuse_questionnaire(aidbox_client, safe_db):
    address = await create_questionnaire(
        aidbox_client,
        {
            "status": "active",
            "launchContext": [
                {
                    "name": {
                        "code": "LaunchPatient",
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                    },
                    "type": ["Patient"],
                }
            ],
            "assembleContext": "prefix",
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
        aidbox_client,
        {
            "status": "active",
            "launchContext": [
                {
                    "name": {
                        "code": "LaunchPatient",
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                    },
                    "type": ["Patient"],
                }
            ],
            "item": [
                {
                    "type": "group",
                    "linkId": "patient-address",
                    "itemPopulationContext": {
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
                    "itemPopulationContext": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.contact",
                    },
                    "item": [
                        {
                            "type": "group",
                            "linkId": "patient-contanct-address",
                            "itemPopulationContext": {
                                "language": "text/fhirpath",
                                "expression": "address",
                            },
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
        "launchContext": [
            {
                "name": {
                    "code": "LaunchPatient",
                    "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                },
                "type": ["Patient"],
            }
        ],
        "item": [
            {
                "type": "group",
                "linkId": "patient-address",
                "itemPopulationContext": {
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
                "itemPopulationContext": {
                    "language": "text/fhirpath",
                    "expression": "%LaunchPatient.contact",
                },
                "item": [
                    {
                        "type": "group",
                        "linkId": "patient-contanct-address",
                        "itemPopulationContext": {
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


@pytest.mark.asyncio
async def test_validate_assemble_context(aidbox_client):
    address = await create_address_questionnaire(aidbox_client)

    q = await create_questionnaire(
        aidbox_client,
        {
            "status": "active",
            "launchContext": [
                {
                    "name": {
                        "code": "LaunchPatient",
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                    },
                    "type": ["Patient"],
                }
            ],
            "item": [
                {
                    "type": "group",
                    "linkId": "patient-address",
                    "itemPopulationContext": {
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
                                    "name": "prefix-not-in-assemble-context",
                                    "language": "text/fhirpath",
                                    "expression": "'patient-address-'",
                                }
                            ],
                            "subQuestionnaire": address.id,
                        }
                    ],
                },
            ],
        },
    )
    with pytest.raises(OperationOutcome):
        await q.execute("$assemble", method="get")


@pytest.mark.asyncio
async def test_assemble_sub_questionnaire_fhir(aidbox_client, safe_db):
    get_given_name = await create_questionnaire(
        aidbox_client,
        {
            "status": "active",
            "launchContext": [
                {
                    "name": {
                        "code": "LaunchPatient",
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                    },
                    "type": ["Patient"],
                }
            ],
            "targetStructureMap": ["StructureMap/create-patient"],
            "itemPopulationContext": {
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
        aidbox_client,
        {
            "status": "active",
            "launchContext": [
                {
                    "name": {
                        "code": "LaunchPatient",
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                    },
                    "type": ["Patient"],
                }
            ],
            "targetStructureMap": ["StructureMap/create-patient"],
            "itemPopulationContext": {
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
        aidbox_client,
        {
            "status": "active",
            "resourceType": "Questionnaire",
            "targetStructureMap": ["StructureMap/create-another-patient"],
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

    assembled = await aidbox_client.execute(f"fhir/Questionnaire/{q['id']}/$assemble", method="get")

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
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
                "extension": [
                    {
                        "url": "name",
                        "valueCoding": {
                            "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            "code": "LaunchPatient",
                            "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        },
                    },
                    {"url": "type", "valueCode": "Patient"},
                ],
            },
            {
                "url": "https://jira.hl7.org/browse/FHIR-22356#assembledFrom",
                "valueCanonical": q.id,
            },
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                "valueCanonical": "StructureMap/create-another-patient",
            },
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
                "valueCanonical": "StructureMap/create-patient",
            },
        ],
    }
