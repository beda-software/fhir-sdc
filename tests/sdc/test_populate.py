import json
from fhirpy.base.exceptions import OperationOutcome
import pytest
from decimal import Decimal
from fhirpathpy import evaluate

from tests.factories import (
    create_questionnaire,
    make_parameters,
    make_launch_context_ext,
    make_initial_expression_ext,
    make_item_population_context_ext,
    make_questionnaire,
    make_source_queries_ext,
    make_variable_ext,
)


@pytest.mark.asyncio
async def test_initial_populate(fhir_client, safe_db):
    """Item with static 'initial' (no initialExpression) is pre-filled in the response."""
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "type": "string",
                    "linkId": "prefilled",
                    "initial": [{"valueString": "prefilled value"}],
                },
            ],
        },
    )

    p = await q.execute("$populate", data=make_parameters())

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {
                "linkId": "prefilled",
                "answer": [{"valueString": "prefilled value"}],
            },
        ],
    }


@pytest.mark.asyncio
async def test_initial_expression_all_answer_types_populate(fhir_client, safe_db):
    """
    Cover all get_type() branches: string, integer, decimal, date, dateTime, time,
    boolean, text, email, phone, display, url, reference, quantity, attachment,
    choice (valueCoding and valueString).
    Uses simple constants or launch context for initial expressions.
    """
    practitioner = fhir_client.resource(
        "Practitioner",
        **{
            "name": [{"family": "Smith", "given": ["John"]}],
        },
    )
    await practitioner.save()

    patient = {
        "resourceType": "Patient",
        "id": "patient-1",
        "generalPractitioner": [{"reference": f"Practitioner/{practitioner['id']}"}],
    }

    observation = fhir_client.resource(
        "Observation",
        **{
            "status": "final",
            "code": {"coding": [{"system": "http://loinc.org", "code": "1234-5"}]},
            "valueQuantity": {
                "value": 100,
                "unit": "mg",
                "system": "http://unitsofmeasure.org",
                "code": "mg",
            },
        },
    )
    await observation.save()

    document_reference = fhir_client.resource(
        "DocumentReference",
        **{
            "status": "current",
            "content": [
                {
                    "attachment": {
                        "contentType": "application/pdf",
                        "url": "http://example.com/doc.pdf",
                    }
                }
            ],
        },
    )
    await document_reference.save()

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("Patient", "Patient"),
                make_launch_context_ext("Observation", "Observation"),
                make_launch_context_ext("DocumentReference", "DocumentReference"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "string",
                    "extension": [make_initial_expression_ext("'string-val'")],
                },
                {
                    "type": "integer",
                    "linkId": "integer",
                    "extension": [make_initial_expression_ext("42")],
                },
                {
                    "type": "decimal",
                    "linkId": "decimal",
                    "extension": [make_initial_expression_ext("3.14")],
                },
                {
                    "type": "date",
                    "linkId": "date",
                    "extension": [make_initial_expression_ext("'2024-01-15'")],
                },
                {
                    "type": "dateTime",
                    "linkId": "dateTime",
                    "extension": [make_initial_expression_ext("'2024-01-15T12:00:00Z'")],
                },
                {
                    "type": "time",
                    "linkId": "time",
                    "extension": [make_initial_expression_ext("'12:30:00'")],
                },
                {
                    "type": "boolean",
                    "linkId": "boolean",
                    "extension": [make_initial_expression_ext("true")],
                },
                {
                    "type": "text",
                    "linkId": "text",
                    "extension": [make_initial_expression_ext("'text-val'")],
                },
                {
                    "type": "display",
                    "linkId": "display",
                    "extension": [make_initial_expression_ext("'display-val'")],
                },
                {
                    "type": "url",
                    "linkId": "url",
                    "extension": [make_initial_expression_ext("'https://example.com'")],
                },
                {
                    "type": "reference",
                    "linkId": "reference",
                    "extension": [
                        make_initial_expression_ext(
                            "%Patient.generalPractitioner.first()"
                        )
                    ],
                },
                {
                    "type": "reference",
                    "linkId": "reference-resource",
                    "extension": [
                        make_initial_expression_ext(
                            "%DocumentReference"
                        )
                    ],
                },
                {
                    "type": "quantity",
                    "linkId": "quantity",
                    "extension": [
                        make_initial_expression_ext("%Observation.valueQuantity")
                    ],
                },
                {
                    "type": "attachment",
                    "linkId": "attachment",
                    "extension": [
                        make_initial_expression_ext(
                            "%DocumentReference.content.attachment.first()"
                        )
                    ],
                },
                {
                    "type": "choice",
                    "linkId": "choice-valueCoding",
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "CODE1",
                                "system": "http://example.org",
                                "display": "Option 1",
                            }
                        },
                    ],
                    "extension": [
                        make_initial_expression_ext(
                            "%qitem.answerOption.valueCoding.first()"
                        )
                    ],
                },
                {
                    "type": "choice",
                    "linkId": "choice-valueString",
                    "answerOption": [{"valueString": "opt-a"}],
                    "extension": [make_initial_expression_ext("'opt-a'")],
                },
            ],
        },
    )

    qr = await q.execute(
        "$populate",
        data=make_parameters(
            Patient=patient,
            Observation=observation,
            DocumentReference=document_reference,
        ),
    )
    await fhir_client.resource("QuestionnaireResponse", **qr).save()

    items = qr["item"]
    by_link_id = {it["linkId"]: it for it in items}

    assert by_link_id["string"]["answer"] == [{"valueString": "string-val"}]
    assert by_link_id["integer"]["answer"] == [{"valueInteger": 42}]
    assert by_link_id["decimal"]["answer"] == [{"valueDecimal": 3.14}]
    assert by_link_id["date"]["answer"] == [{"valueDate": "2024-01-15"}]
    assert by_link_id["dateTime"]["answer"] == [{"valueDateTime": "2024-01-15T12:00:00Z"}]
    assert by_link_id["time"]["answer"] == [{"valueTime": "12:30:00"}]
    assert by_link_id["boolean"]["answer"] == [{"valueBoolean": True}]
    assert by_link_id["text"]["answer"] == [{"valueString": "text-val"}]
    assert by_link_id["display"]["answer"] == [{"valueString": "display-val"}]
    assert by_link_id["url"]["answer"] == [{"valueUri": "https://example.com"}]
    ref_answer = by_link_id["reference"]["answer"][0].get("valueReference")
    assert ref_answer.get("reference") == f"Practitioner/{practitioner['id']}"
    ref_resource_answer = by_link_id["reference-resource"]["answer"][0].get(
        "valueReference"
    )
    assert ref_resource_answer.get("reference") == f"DocumentReference/{document_reference['id']}"
    assert by_link_id["quantity"]["answer"] == [
        {
            "valueQuantity": {
                "value": 100,
                "unit": "mg",
                "system": "http://unitsofmeasure.org",
                "code": "mg",
            }
        }
    ]
    assert by_link_id["attachment"]["answer"] == [
        {
            "valueAttachment": {
                "contentType": "application/pdf",
                "url": "http://example.com/doc.pdf",
            }
        }
    ]
    assert by_link_id["choice-valueCoding"]["answer"] == [
        {
            "valueCoding": {
                "code": "CODE1",
                "system": "http://example.org",
                "display": "Option 1",
            }
        }
    ]
    assert by_link_id["choice-valueString"]["answer"] == [{"valueString": "opt-a"}]


@pytest.mark.asyncio
async def test_initial_expression_populate(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                    "extension": [make_initial_expression_ext("%LaunchPatient.id")],
                },
            ],
        },
    )

    launch_patient = {"resourceType": "Patient", "id": "patienit-id"}

    p = await q.execute(
        "$populate", data=make_parameters(LaunchPatient=launch_patient)
    )

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {
                "linkId": "patientId",
                "answer": [{"valueString": launch_patient["id"]}],
            }
        ],
    }


@pytest.mark.asyncio
async def test_initial_expression_populate_using_list_endpoint(fhir_client, safe_db):
    q = make_questionnaire({
        "id": "virtual-id",
        "resourceType": "Questionnaire",
        "status": "active",
        "extension": [make_launch_context_ext("LaunchPatient", "Patient")],
        "item": [
            {
                "type": "string",
                "linkId": "patientId",
                "extension": [make_initial_expression_ext("%LaunchPatient.id")],
            },
        ],
    })

    launch_patient = {"resourceType": "Patient", "id": "patient-id"}

    p = await fhir_client.execute(
        "Questionnaire/$populate",
        data=make_parameters(Questionnaire=q, LaunchPatient=launch_patient),
    )

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q["id"],
        "item": [
            {
                "linkId": "patientId",
                "answer": [{"valueString": launch_patient["id"]}],
            }
        ],
    }


@pytest.mark.asyncio
async def test_item_context_with_repeats_populate(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_item_population_context_ext("%LaunchPatient.name"),
            ],
            "item": [
                {
                    "type": "group",
                    "linkId": "names",
                    "extension": [
                        make_item_population_context_ext("%LaunchPatient.name")
                    ],
                    "item": [
                        {
                            "repeats": True,
                            "type": "string",
                            "linkId": "firstName",
                            "extension": [make_initial_expression_ext("given")],
                        },
                    ],
                },
            ],
        },
    )


    launch_patient = {
        "resourceType": "Patient",
        "id": "patienit-id",
        "name": [
            {"given": ["Peter", "Middlename"]},
            {"given": ["Pit"]},
            {"given": ["Little Pitty"]},
        ],
    }

    p = await q.execute(
        "$populate", data=make_parameters(LaunchPatient=launch_patient)
    )

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "firstName",
                        "answer": [
                            {"valueString": "Peter"},
                            {"valueString": "Middlename"},
                            {"valueString": "Pit"},
                            {"valueString": "Little Pitty"},
                        ],
                    }
                ],
                "linkId": "names",
            }
        ],
        "questionnaire": q.id,
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
    }


@pytest.mark.asyncio
async def test_item_context_with_repeating_group_populate(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_item_population_context_ext("%LaunchPatient.address"),
            ],
            "item": [
                {
                    "type": "group",
                    "linkId": "addresses",
                    "repeats": True,
                    "extension": [
                        make_item_population_context_ext("%LaunchPatient.address")
                    ],
                    "item": [
                        {
                            "type": "string",
                            "linkId": "city",
                            "extension": [make_initial_expression_ext("city.first()")],
                        },
                    ],
                },
            ],
        },
    )

    launch_patient = {
        "resourceType": "Patient",
        "id": "patienit-id",
        "address": [{"city": "San Francisco"}, {"city": "San Diego"}],
    }

    p = await q.execute(
        "$populate", data=make_parameters(LaunchPatient=launch_patient)
    )

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "city",
                        "answer": [
                            {"valueString": "San Francisco"},
                        ],
                    }
                ],
                "linkId": "addresses",
            },
            {
                "item": [
                    {
                        "linkId": "city",
                        "answer": [
                            {"valueString": "San Diego"},
                        ],
                    }
                ],
                "linkId": "addresses",
            },
        ],
        "questionnaire": q.id,
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
    }


@pytest.mark.asyncio
async def test_item_context_with_repeating_group_populate_from_nonlocal_context(
    fhir_client, safe_db
):
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_launch_context_ext("LaunchEncounter", "Encounter"),
            ],
            "item": [
                {
                    "type": "group",
                    "linkId": "addresses",
                    "repeats": True,
                    "extension": [
                        make_item_population_context_ext("%LaunchPatient.address")
                    ],
                    "item": [
                        {
                            "type": "string",
                            "linkId": "city",
                            "extension": [make_initial_expression_ext("city.first()")],
                        },
                        {
                            "type": "string",
                            "repeats": True,
                            "linkId": "encounter-id",
                            "extension": [
                                make_initial_expression_ext("%LaunchEncounter.id")
                            ],
                        },
                    ],
                },
            ],
        },
    )

    launch_patient = {
        "resourceType": "Patient",
        "id": "patienit-id",
        "address": [{"city": "San Francisco"}, {"city": "San Diego"}],
    }

    launch_encounter = {"resourceType": "Encounter", "id": "encounter-example"}

    p = await q.execute(
        "$populate",
        data=make_parameters(
            LaunchPatient=launch_patient, LaunchEncounter=launch_encounter
        ),
    )

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "city",
                        "answer": [
                            {"valueString": "San Francisco"},
                        ],
                    },
                    {
                        "linkId": "encounter-id",
                        "answer": [
                            {"valueString": "encounter-example"},
                        ],
                    },
                ],
                "linkId": "addresses",
            },
            {
                "item": [
                    {
                        "linkId": "city",
                        "answer": [
                            {"valueString": "San Diego"},
                        ],
                    },
                    {
                        "linkId": "encounter-id",
                        "answer": [
                            {"valueString": "encounter-example"},
                        ],
                    },
                ],
                "linkId": "addresses",
            },
        ],
        "questionnaire": q.id,
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
    }


@pytest.mark.asyncio
async def test_item_context_without_repeats_populate(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_item_population_context_ext("%LaunchPatient.address"),
            ],
            "item": [
                {
                    "text": "Address",
                    "type": "group",
                    "linkId": "address",
                    "extension": [
                        make_item_population_context_ext("%LaunchPatient.address")
                    ],
                    "item": [
                        {
                            "text": "City",
                            "linkId": "city",
                            "type": "string",
                            "extension": [make_initial_expression_ext("city")],
                        },
                        {
                            "text": "Line 1",
                            "linkId": "line-1",
                            "type": "string",
                            "extension": [make_initial_expression_ext("line[0]")],
                        },
                        {
                            "text": "Line 2",
                            "linkId": "line-2",
                            "type": "string",
                            "extension": [make_initial_expression_ext("line[1]")],
                        },
                        {
                            "text": "Country",
                            "linkId": "Country",
                            "type": "string",
                            "extension": [make_initial_expression_ext("country")],
                        },
                    ],
                }
            ],
        },
    )

    launch_patient = {
        "resourceType": "Patient",
        "id": "patienit-id",
        "address": [
            {
                "city": "Sydney",
                "line": ["Central park", "near metro station museum"],
                "country": "Australia",
            }
        ],
    }

    p = await q.execute(
        "$populate", data=make_parameters(LaunchPatient=launch_patient)
    )

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "answer": [{"valueString": "Sydney"}],
                        "linkId": "city",
                        "text": "City",
                    },
                    {
                        "answer": [{"valueString": "Central park"}],
                        "linkId": "line-1",
                        "text": "Line 1",
                    },
                    {
                        "answer": [{"valueString": "near metro station museum"}],
                        "linkId": "line-2",
                        "text": "Line 2",
                    },
                    {
                        "answer": [{"valueString": "Australia"}],
                        "linkId": "Country",
                        "text": "Country",
                    },
                ],
                "linkId": "address",
                "text": "Address",
            }
        ],
        "questionnaire": q.id,
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
    }


@pytest.mark.asyncio
async def test_source_query_populate(fhir_client, safe_db):
    p = fhir_client.resource("Patient")
    await p.save()

    a = fhir_client.resource(
        "Appointment",
        **{
            "status": "booked",
            "start": "2020-01-01T00:00:00Z",
            "end": "2020-01-01T00:30:00Z",
            "participant": [{"status": "accepted", "actor": p}],
        },
    )
    await a.save()

    q = await create_questionnaire(
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

    p = await q.execute("$populate", data=make_parameters(LaunchPatient=p))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {
                "linkId": "last-appointment",
                "answer": [{"valueString": a["start"]}],
            }
        ],
    }


@pytest.mark.asyncio
async def test_multiple_answers_populate(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("Diet", "Bundle"),
            ],
            "item": [
                {
                    "type": "choice",
                    "linkId": "diet",
                    "repeats": True,
                    "extension": [
                        make_initial_expression_ext(
                            "%Diet.entry.resource.oralDiet.type.coding.where(system = 'http://snomed.info/sct')"
                        )
                    ],
                },
            ],
        },
    )

    diet = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {
                    "resourceType": "NutritionOrder",
                    "oralDiet": {
                        "type": {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "160671006",
                                },
                            ]
                        },
                    },
                },
            },
            {
                "resource": {
                    "resourceType": "NutritionOrder",
                    "oralDiet": {
                        "type": {
                            "coding": [
                                {
                                    "system": "UNKNOWN",
                                    "code": "ABC",
                                },
                            ]
                        },
                    },
                },
            },
            {
                "resource": {
                    "resourceType": "NutritionOrder",
                    "oralDiet": {
                        "type": {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "302320003",
                                },
                            ]
                        },
                    },
                },
            },
        ],
    }

    p = await q.execute("$populate", data=make_parameters(Diet=diet))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {
                "linkId": "diet",
                "answer": [
                    {
                        "valueCoding": {
                            "system": "http://snomed.info/sct",
                            "code": "160671006",
                        }
                    },
                    {
                        "valueCoding": {
                            "system": "http://snomed.info/sct",
                            "code": "302320003",
                        }
                    },
                ],
            }
        ],
    }


@pytest.mark.asyncio
async def test_fhirpath_failure_populate(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        {
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientName",
                    "extension": [
                        make_initial_expression_ext(
                            "%LaunchPatient.name.given.toQuantity()"
                        )
                    ],
                }
            ],
            "status": "active",
        },
    )

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "name": [{"given": ["Peter", "James"], "family": "Chalmers"}],
    }

    try:
        await q.execute(
            "$populate", data=make_parameters(LaunchPatient=launch_patient)
        )
    except Exception as e:
        assert json.loads(str(e)) == {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "fatal",
                    "code": "invalid",
                    "diagnostics": 'Error: "%LaunchPatient.name.given.toQuantity()" - Could not convert to quantity: input collection contains multiple items',
                }
            ],
            "text": {
                "status": "generated",
                "div": 'Error: "%LaunchPatient.name.given.toQuantity()" - Could not convert to quantity: input collection contains multiple items',
            },
        }
        return
    assert False


@pytest.mark.asyncio
async def test_fhirpath_success_populate(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        {
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientName",
                    "extension": [
                        make_initial_expression_ext(
                            "%LaunchPatient.name.given[0] + ' ' + %LaunchPatient.name.family"
                        )
                    ],
                }
            ],
            "status": "active",
        },
    )

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "name": [{"given": ["Peter", "James"], "family": "Chalmers"}],
    }

    p = await q.execute(
        "$populate", data=make_parameters(LaunchPatient=launch_patient)
    )

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {"linkId": "patientName", "answer": [{"valueString": "Peter Chalmers"}]}
        ],
    }


@pytest.mark.asyncio
async def test_money_populate(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        {
            "item": [
                {
                    "type": "quantity",
                    "linkId": "charge-amount",
                    "extension": [
                        make_initial_expression_ext(
                            "%ChargeItemDefinition.extension('charge-item-definition-price').valueQuantity"
                        )
                    ],
                }
            ],
            "status": "active",
            "resourceType": "Questionnaire",
            "extension": [
                make_launch_context_ext("ChargeItemDefinition", "ChargeItemDefinition")
            ],
        },
    )

    charge_item_definition = {
        "resourceType": "ChargeItemDefinition",
        "extension": [
            {
                "url": "charge-item-definition-price",
                "valueQuantity": {
                    "code": "USD",
                    "value": 33.3,
                    "system": "urn:iso:std:iso:4217",
                },
            }
        ],
    }

    p = await q.execute(
        "$populate",
        data=make_parameters(ChargeItemDefinition=charge_item_definition),
    )

    assert evaluate(
        p,
        "QuestionnaireResponse.item.where(linkId='charge-amount').answer.valueQuantity",
    ) == [{"code": "USD", "system": "urn:iso:std:iso:4217", "value": Decimal("33.3")}]


@pytest.mark.asyncio
async def test_source_query_with_qr_vars_populate(fhir_client, safe_db):
    """
    It's unusual case according to FHIR SDC spec, but we use QR vars in source queries for constraint checks
    The test checks that populate does not fail when we access QR
    """

    p = fhir_client.resource("Patient")
    await p.save()

    q = await create_questionnaire(
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
                                "url": "Appointment?patient={{(%QuestionnaireResponse.item.where(linkId='patient-id').answer.valueString | 'undefined').first()}}",
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
                    # Constraint check that uses PrePopQuery should go here
                },
            ],
        },
    )

    p = await q.execute("$populate", data=make_parameters(LaunchPatient=p))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [{"linkId": "last-appointment"}],
    }


@pytest.mark.asyncio
async def test_initial_expression_questionnaire_env_populate(fhir_client, safe_db):
    """
    In initial expressions, %questionnaire points to the Questionnaire 
    """
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "type": "choice",
                    "linkId": "q-1",
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "ABC",
                                "system": "http://example.org",
                                "display": "Option ABC",
                            }
                        },   
                    ],
                    "extension": [
                        make_initial_expression_ext(
                            "%questionnaire.item.where(linkId='q-1').answerOption.valueCoding.first()"
                        )
                    ],
                },
            ],
        },
    )

    p = await q.execute("$populate", data=make_parameters())

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {"linkId": "q-1", "answer": [{"valueCoding": {"code": "ABC", "system": "http://example.org", "display": "Option ABC"}}]},
        ],
    }


@pytest.mark.asyncio
async def test_initial_expression_qitem_env_populate(fhir_client, safe_db):
    """
    In initial expressions, %qitem points to the current question item definition.
    Same content in q-1 (root) and q-2 (inside g-1): each uses %qitem to get its own answerOption.
    """
    q_item_with_qitem = {
        "type": "choice",
        "answerOption": [
            {
                "valueCoding": {
                    "code": "FROM_QITEM",
                    "system": "http://example.org",
                    "display": "From qitem",
                }
            },
        ],
        "extension": [
            make_initial_expression_ext(
                "%qitem.answerOption.valueCoding.first()"
            )
        ],
    }
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {**q_item_with_qitem, "linkId": "q-1"},
                {
                    "type": "group",
                    "linkId": "g-1",
                    "item": [
                        {**q_item_with_qitem, "linkId": "q-2"},
                    ],
                },
            ],
        },
    )

    p = await q.execute("$populate", data=make_parameters())

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {
                "linkId": "q-1",
                "answer": [{"valueCoding": {"code": "FROM_QITEM", "system": "http://example.org", "display": "From qitem"}}],
            },
            {
                "linkId": "g-1",
                "item": [
                    {
                        "linkId": "q-2",
                        "answer": [{"valueCoding": {"code": "FROM_QITEM", "system": "http://example.org", "display": "From qitem"}}],
                    }
                ],
            },
        ],
    }


@pytest.mark.asyncio
async def test_initial_expression_resource_env_populate(fhir_client, safe_db):
    """
    In initial expressions, %resource points to the QuestionnaireResponse being built. 
    """
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "type": "string",
                    "linkId": "q-1",
                    "extension": [make_initial_expression_ext("'constant'")],
                },
                {
                    "type": "string",
                    "linkId": "q-2",
                    "extension": [
                        make_initial_expression_ext(
                            "%resource.item.where(linkId='q-1').answer.valueString.first()"
                        )
                    ],
                },
            ],
        },
    )

    p = await q.execute("$populate", data=make_parameters())

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {"linkId": "q-1", "answer": [{"valueString": "constant"}]},
            {"linkId": "q-2", "answer": [{"valueString": "constant"}]},
        ],
    }


@pytest.mark.asyncio
async def test_variable_root_level_populate(fhir_client, safe_db):
    """
    Variables on Questionnaire root and then use in initial expression.
    """
    patient = {"resourceType": "Patient", "id": "patient-123"}
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("patient", "Patient"),
                make_variable_ext("PatientId", "%patient.id"),
                make_variable_ext("PatientReference", "'Patient/' + %PatientId"),
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "q-1",
                    "extension": [
                        make_initial_expression_ext("%PatientReference"),
                    ],
                },
            ],
        },
    )

    p = await q.execute("$populate", data=make_parameters(patient=patient))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {"linkId": "q-1", "answer": [{"valueString": "Patient/patient-123"}]},
        ],
    }


@pytest.mark.asyncio
async def test_variable_question_level_populate(fhir_client, safe_db):
    """
    Variables on question level and then use in initial expression.
    """
    patient = {"resourceType": "Patient", "id": "patient-456"}
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_launch_context_ext("patient", "Patient")],
            "item": [
                {
                    "type": "string",
                    "linkId": "q-1",
                    "extension": [
                        make_variable_ext("PatientId", "%patient.id"),
                        make_variable_ext("PatientReference", "'Patient/' + %PatientId"),
                        make_initial_expression_ext("%PatientReference"),
                    ],
                },
            ],
        },
    )

    p = await q.execute("$populate", data=make_parameters(patient=patient))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {"linkId": "q-1", "answer": [{"valueString": "Patient/patient-456"}]},
        ],
    }


@pytest.mark.asyncio
async def test_variable_group_level_populate(fhir_client, safe_db):
    """
    Variables on group level and then use in initial expression.
    """
    patient = {"resourceType": "Patient", "id": "patient-789"}
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_launch_context_ext("patient", "Patient")],
            "item": [
                {
                    "type": "group",
                    "linkId": "g-1",
                    "extension": [
                        make_variable_ext("PatientId", "%patient.id"),
                        make_variable_ext("PatientReference", "'Patient/' + %PatientId"),
                    ],
                    "item": [
                        {
                            "type": "string",
                            "linkId": "q-1",
                            "extension": [
                                make_initial_expression_ext("%PatientReference"),
                            ],
                        },
                    ],
                },
            ],
        },
    )

    p = await q.execute("$populate", data=make_parameters(patient=patient))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": q.id,
        "item": [
            {
                "linkId": "g-1",
                "item": [
                    {"linkId": "q-1", "answer": [{"valueString": "Patient/patient-789"}]},
                ],
            },
        ],
    }


@pytest.mark.asyncio
async def test_variable_defined_in_one_group_not_visible_in_sibling_group_populate(
    fhir_client, safe_db
):
    """
    Variable defined in one group must not be visible in a sibling group.
    """
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "type": "group",
                    "linkId": "g-first",
                    "extension": [
                        make_variable_ext("SiblingVar", "'from-first-group'"),
                    ],
                    "item": [
                        {
                            "type": "string",
                            "linkId": "q-in-first",
                            "extension": [
                                make_initial_expression_ext("%SiblingVar"),
                            ],
                        },
                    ],
                },
                {
                    "type": "group",
                    "linkId": "g-second",
                    "item": [
                        {
                            "type": "string",
                            "linkId": "q-in-second",
                            "extension": [
                                make_initial_expression_ext("%SiblingVar"),
                            ],
                        },
                    ],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome) as exc:
        await q.execute("$populate", data=make_parameters())
        assert exc.value.resource["issue"][0]["code"] == "invalid"
