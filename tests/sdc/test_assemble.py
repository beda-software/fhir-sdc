import pytest
from fhirpy.base.exceptions import OperationOutcome

from tests.factories import (
    create_address_questionnaire,
    create_questionnaire,
    make_assemble_context_ext,
    make_assembled_from_ext,
    make_cqf_library_ext,
    make_initial_expression_ext,
    make_item_population_context_ext,
    make_launch_context_ext,
    make_questionnaire_mapper_ext,
    make_source_queries_ext,
    make_sub_questionnaire_ext,
    make_target_structure_map_ext,
    make_variable_ext,
)


@pytest.mark.asyncio
async def test_assemble_sub_questionnaire(fhir_client, safe_db):
    get_given_name = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_item_population_context_ext("%LaunchPatient.name"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "firstName",
                    "extension": [make_initial_expression_ext("given.first()")],
                },
            ],
        },
    )

    get_family_name = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_item_population_context_ext("%LaunchPatient.name"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "familyName",
                    "extension": [make_initial_expression_ext("family")],
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
                            "extension": [make_sub_questionnaire_ext(get_given_name.id)],
                        },
                        {
                            "type": "display",
                            "linkId": "familyNameGroup",
                            "text": "Sub questionnaire is not supported",
                            "extension": [make_sub_questionnaire_ext(get_family_name.id)],
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
            make_launch_context_ext("LaunchPatient", "Patient"),
            make_assembled_from_ext(q.id),
        ],
        "item": [
            {
                "linkId": "demographics",
                "type": "group",
                "extension": [make_item_population_context_ext("%LaunchPatient.name")],
                "item": [
                    {
                        "type": "string",
                        "linkId": "firstName",
                        "extension": [make_initial_expression_ext("given.first()")],
                    },
                    {
                        "type": "string",
                        "linkId": "familyName",
                        "extension": [make_initial_expression_ext("family")],
                    },
                ],
            }
        ],
    }


@pytest.mark.asyncio
async def test_fhir_assemble_sub_questionnaire(fhir_client, safe_db):
    # This test is very similar to the test_assemble_sub_questionnaire test,
    # but it has a bit more functionality
    # TODO: think about getting rid the previous one
    get_given_name = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_target_structure_map_ext("StructureMap/create-patient"),
                make_item_population_context_ext("%LaunchPatient.name"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "firstName",
                    "extension": [make_initial_expression_ext("given.first()")],
                },
            ],
        },
    )

    get_family_name = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_target_structure_map_ext("StructureMap/create-patient"),
                make_item_population_context_ext("%LaunchPatient.name"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "familyName",
                    "extension": [make_initial_expression_ext("family")],
                },
            ],
        },
    )

    get_line2_address = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_target_structure_map_ext("StructureMap/create-patient"),
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
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_target_structure_map_ext("StructureMap/create-patient"),
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
                    "extension": [make_sub_questionnaire_ext(get_line2_address.id)],
                },
            ],
        },
    )

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "resourceType": "Questionnaire",
            "extension": [make_target_structure_map_ext("StructureMap/create-another-patient")],
            "item": [
                {
                    "linkId": "demographics",
                    "type": "group",
                    "item": [
                        {
                            "type": "display",
                            "linkId": "givenNameGroup",
                            "text": "Sub questionnaire is not supported",
                            "extension": [make_sub_questionnaire_ext(get_given_name.id)],
                        },
                        {
                            "type": "display",
                            "linkId": "familyNameGroup",
                            "text": "Sub questionnaire is not supported",
                            "extension": [make_sub_questionnaire_ext(get_family_name.id)],
                        },
                        {
                            "type": "display",
                            "linkId": "address",
                            "text": "Sub questionnaire",
                            "extension": [make_sub_questionnaire_ext(get_address.id)],
                        },
                    ],
                }
            ],
        },
    )

    assembled = await q.execute("$assemble", method="get")

    del assembled["meta"]

    assert assembled == {
        "item": [
            {
                "item": [
                    {
                        "type": "string",
                        "linkId": "firstName",
                        "extension": [make_initial_expression_ext("given.first()")],
                    },
                    {
                        "type": "string",
                        "linkId": "familyName",
                        "extension": [make_initial_expression_ext("family")],
                    },
                    {"type": "string", "linkId": "line-1"},
                    {"type": "string", "linkId": "address-line-2"},
                ],
                "type": "group",
                "linkId": "demographics",
                "extension": [make_item_population_context_ext("%LaunchPatient.name")],
            }
        ],
        "status": "active",
        "resourceType": "Questionnaire",
        "extension": [
            make_launch_context_ext("LaunchPatient", "Patient"),
            make_target_structure_map_ext("StructureMap/create-another-patient"),
            make_target_structure_map_ext("StructureMap/create-patient"),
            make_assembled_from_ext(q["id"]),
        ],
    }


@pytest.mark.asyncio
async def test_assemble_double_nested_sub_questionnaire(fhir_client, safe_db):
    m1 = fhir_client.resource("Mapping", body={"resourceType": "Bundle", "type": "transaction"})
    await m1.save()
    m2 = fhir_client.resource("Mapping", body={"resourceType": "Bundle", "type": "transaction"})
    await m2.save()
    m3 = fhir_client.resource("Mapping", body={"resourceType": "Bundle", "type": "transaction"})
    await m3.save()

    get_family_name = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_item_population_context_ext("%LaunchPatient.name"),
                make_questionnaire_mapper_ext(m3.id),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "familyName",
                    "extension": [make_initial_expression_ext("family")],
                },
            ],
        },
    )

    get_given_name = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_item_population_context_ext("%LaunchPatient.name"),
                make_questionnaire_mapper_ext(m2.id),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "firstName",
                    "extension": [make_initial_expression_ext("given.first()")],
                },
                {
                    "type": "display",
                    "linkId": "familyNameGroup",
                    "text": "Sub questionnaire is not supported",
                    "extension": [make_sub_questionnaire_ext(get_family_name.id)],
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
                make_questionnaire_mapper_ext(m1.id),
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
                            "extension": [make_sub_questionnaire_ext(get_given_name.id)],
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
            make_launch_context_ext("LaunchPatient", "Patient"),
            make_questionnaire_mapper_ext(m1.id),
            make_questionnaire_mapper_ext(m2.id),
            make_questionnaire_mapper_ext(m3.id),
            make_assembled_from_ext(q.id),
        ],
        "item": [
            {
                "linkId": "demographics",
                "type": "group",
                "extension": [make_item_population_context_ext("%LaunchPatient.name")],
                "item": [
                    {
                        "type": "string",
                        "linkId": "firstName",
                        "extension": [make_initial_expression_ext("given.first()")],
                    },
                    {
                        "type": "string",
                        "linkId": "familyName",
                        "extension": [make_initial_expression_ext("family")],
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
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_assemble_context_ext("prefix"),
            ],
            "item": [
                {
                    "linkId": "{{%prefix}}line-1",
                    "type": "string",
                    "extension": [make_initial_expression_ext("line[0]")],
                },
                {
                    "linkId": "{{%prefix}}line-2",
                    "type": "string",
                    "extension": [make_initial_expression_ext("line[1]")],
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
            "extension": [make_launch_context_ext("LaunchPatient", "Patient")],
            "item": [
                {
                    "type": "group",
                    "linkId": "patient-address",
                    "extension": [make_item_population_context_ext("%LaunchPatient.address")],
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
                    "extension": [make_item_population_context_ext("%LaunchPatient.contact")],
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
                                        make_variable_ext("prefix", "'patient-contact-address-'"),
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

    del assembled["meta"]

    assert assembled == {
        "resourceType": "Questionnaire",
        "status": "active",
        "extension": [
            make_launch_context_ext("LaunchPatient", "Patient"),
            make_assembled_from_ext(q.id),
        ],
        "item": [
            {
                "type": "group",
                "linkId": "patient-address",
                "extension": [make_item_population_context_ext("%LaunchPatient.address")],
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
                "extension": [make_item_population_context_ext("%LaunchPatient.contact")],
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


@pytest.mark.asyncio
async def test_validate_assemble_context(fhir_client, safe_db):
    address = await create_address_questionnaire(fhir_client)

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_launch_context_ext("LaunchPatient", "Patient")],
            "item": [
                {
                    "type": "group",
                    "linkId": "patient-address",
                    "extension": [make_item_population_context_ext("%LaunchPatient.address")],
                    "item": [
                        {
                            "linkId": "patient-address-display",
                            "type": "display",
                            "text": "Sub questionanire is not supported",
                            "extension": [
                                make_variable_ext(
                                    "prefix-not-in-assemble-context",
                                    "'patient-address-'",
                                ),
                                make_sub_questionnaire_ext(address.id),
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
async def test_assemble_propagates_mapping(fhir_client, safe_db):
    m1 = fhir_client.resource("Mapping", body={"resourceType": "Bundle", "type": "transaction"})
    await m1.save()
    m2 = fhir_client.resource("Mapping", body={"resourceType": "Bundle", "type": "transaction"})
    await m2.save()

    sub1 = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_questionnaire_mapper_ext(m1.id)],
            "item": [{"type": "string", "linkId": "q1"}],
        },
    )
    sub2 = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_questionnaire_mapper_ext(m1.id),
                make_questionnaire_mapper_ext(m2.id),
            ],
            "item": [{"type": "string", "linkId": "q2"}],
        },
    )

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "type": "display",
                    "linkId": "sub1-placeholder",
                    "text": "Sub questionnaire is not supported",
                    "extension": [make_sub_questionnaire_ext(sub1.id)],
                },
                {
                    "type": "display",
                    "linkId": "sub2-placeholder",
                    "text": "Sub questionnaire is not supported",
                    "extension": [make_sub_questionnaire_ext(sub2.id)],
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
            make_questionnaire_mapper_ext(m1.id),
            make_questionnaire_mapper_ext(m2.id),
            make_assembled_from_ext(q.id),
        ],
        "item": [
            {"type": "string", "linkId": "q1"},
            {"type": "string", "linkId": "q2"},
        ],
    }


@pytest.mark.asyncio
async def test_assemble_propagates_source_queries(fhir_client, safe_db):
    sub1 = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_source_queries_ext("#bundle-1")],
            "item": [{"type": "string", "linkId": "q1"}],
        },
    )
    sub2 = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_source_queries_ext("#bundle-1"),
                make_source_queries_ext("#bundle-2"),
            ],
            "item": [{"type": "string", "linkId": "q2"}],
        },
    )

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "type": "display",
                    "linkId": "sub1-placeholder",
                    "text": "Sub questionnaire is not supported",
                    "extension": [make_sub_questionnaire_ext(sub1.id)],
                },
                {
                    "type": "display",
                    "linkId": "sub2-placeholder",
                    "text": "Sub questionnaire is not supported",
                    "extension": [make_sub_questionnaire_ext(sub2.id)],
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
            make_source_queries_ext("#bundle-1"),
            make_source_queries_ext("#bundle-2"),
            make_assembled_from_ext(q.id),
        ],
        "item": [
            {"type": "string", "linkId": "q1"},
            {"type": "string", "linkId": "q2"},
        ],
    }


@pytest.mark.asyncio
async def test_assemble_propagates_contained(fhir_client, safe_db):
    contained_resource = {
        "id": "PrePopQuery",
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [{"request": {"method": "GET", "url": "Patient?_id=1"}}],
    }
    sub = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "contained": [contained_resource],
            "extension": [make_source_queries_ext("#PrePopQuery")],
            "item": [{"type": "string", "linkId": "q1"}],
        },
    )

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "type": "display",
                    "linkId": "sub-placeholder",
                    "text": "Sub questionnaire is not supported",
                    "extension": [make_sub_questionnaire_ext(sub.id)],
                }
            ],
        },
    )

    assembled = await q.execute("$assemble", method="get")

    contained = assembled.get("contained", [])
    assert len(contained) == 1
    assert contained[0]["id"] == "PrePopQuery"
    assert contained[0]["resourceType"] == "Bundle"
    assert {"type": "string", "linkId": "q1"} in assembled["item"]


@pytest.mark.asyncio
async def test_assemble_propagates_cqf_library(fhir_client, safe_db):
    sub = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_cqf_library_ext("http://example.org/Library/MyLib")],
            "item": [{"type": "string", "linkId": "q1"}],
        },
    )

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "type": "display",
                    "linkId": "sub-placeholder",
                    "text": "Sub questionnaire is not supported",
                    "extension": [make_sub_questionnaire_ext(sub.id)],
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
            make_cqf_library_ext("http://example.org/Library/MyLib"),
            make_assembled_from_ext(q.id),
        ],
        "item": [{"type": "string", "linkId": "q1"}],
    }
