import json
import pytest
from decimal import Decimal
from fhirpathpy import evaluate

from app.test.utils import create_parameters
from tests.test_utils import (
    make_launch_context_ext,
    make_initial_expression_ext,
    make_item_population_context_ext,
    make_source_queries_ext,
)


@pytest.mark.asyncio
async def test_initial_expression_populate(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
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
    await q.save()

    assert q.id is not None

    launch_patient = {"resourceType": "Patient", "id": "patienit-id"}

    p = await q.execute(
        "$populate", data=create_parameters(LaunchPatient=launch_patient)
    )

    assert p == {
        "resourceType": "QuestionnaireResponse",
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
    q = {
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
    }

    launch_patient = {"resourceType": "Patient", "id": "patient-id"}

    p = await fhir_client.execute(
        "Questionnaire/$populate",
        data=create_parameters(Questionnaire=q, LaunchPatient=launch_patient),
    )

    assert p == {
        "resourceType": "QuestionnaireResponse",
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
    q = fhir_client.resource(
        "Questionnaire",
        **{
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
    await q.save()

    assert q.id is not None

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
        "$populate", data=create_parameters(LaunchPatient=launch_patient)
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
    }


@pytest.mark.asyncio
async def test_item_context_with_repeating_group_populate(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
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
    await q.save()

    assert q.id is not None

    launch_patient = {
        "resourceType": "Patient",
        "id": "patienit-id",
        "address": [{"city": "San Francisco"}, {"city": "San Diego"}],
    }

    p = await q.execute(
        "$populate", data=create_parameters(LaunchPatient=launch_patient)
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
    }


@pytest.mark.asyncio
async def test_item_context_with_repeating_group_populate_from_nonlocal_context(
    fhir_client, safe_db
):
    q = fhir_client.resource(
        "Questionnaire",
        **{
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
    await q.save()

    assert q.id is not None

    launch_patient = {
        "resourceType": "Patient",
        "id": "patienit-id",
        "address": [{"city": "San Francisco"}, {"city": "San Diego"}],
    }

    launch_encounter = {"resourceType": "Encounter", "id": "encounter-example"}

    p = await q.execute(
        "$populate",
        data=create_parameters(
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
    }


@pytest.mark.asyncio
async def test_item_context_without_repeats_populate(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
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
    await q.save()

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
        "$populate", data=create_parameters(LaunchPatient=launch_patient)
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
            "participant": [{"status": "accepted", "actor": p}],
        },
    )
    await a.save()

    q = fhir_client.resource(
        "Questionnaire",
        **{
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

    await q.save()

    p = await q.execute("$populate", data=create_parameters(LaunchPatient=p))

    assert p == {
        "resourceType": "QuestionnaireResponse",
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
    q = fhir_client.resource(
        "Questionnaire",
        **{
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
    await q.save()

    assert q.id is not None

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

    p = await q.execute("$populate", data=create_parameters(Diet=diet))

    assert p == {
        "resourceType": "QuestionnaireResponse",
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
    q = fhir_client.resource(
        "Questionnaire",
        **{
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
    await q.save()

    assert q.id is not None

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "name": [{"given": ["Peter", "James"], "family": "Chalmers"}],
    }

    try:
        await q.execute(
            "$populate", data=create_parameters(LaunchPatient=launch_patient)
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
    q = fhir_client.resource(
        "Questionnaire",
        **{
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
    await q.save()

    assert q.id is not None

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "name": [{"given": ["Peter", "James"], "family": "Chalmers"}],
    }

    p = await q.execute(
        "$populate", data=create_parameters(LaunchPatient=launch_patient)
    )

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": q.id,
        "item": [
            {"linkId": "patientName", "answer": [{"valueString": "Peter Chalmers"}]}
        ],
    }


@pytest.mark.asyncio
async def test_money_populate(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
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

    await q.save()

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
        data=create_parameters(ChargeItemDefinition=charge_item_definition),
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

    q = fhir_client.resource(
        "Questionnaire",
        **{
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

    await q.save()

    p = await q.execute("$populate", data=create_parameters(LaunchPatient=p))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": q.id,
        "item": [{"linkId": "last-appointment"}],
    }
