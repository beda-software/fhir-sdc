import json

import pytest

from app.test.utils import create_parameters


@pytest.mark.asyncio
async def test_initial_expression_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [
                {
                    "name": "LaunchPatient",
                    "type": "Patient",
                },
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.id",
                    },
                },
            ],
        },
    )
    await q.save()

    assert q.id is not None

    launch_patient = {"resourceType": "Patient", "id": "patienit-id"}

    p = await q.execute("$populate", data=create_parameters(LaunchPatient=launch_patient))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": q.id,
        "item": [
            {
                "linkId": "patientId",
                "answer": [{"value": {"string": launch_patient["id"]}}],
            }
        ],
    }


@pytest.mark.asyncio
async def test_initial_expression_populate_using_list_endpoint(aidbox_client, safe_db):
    q = {
        "id": "virtual-id",
        "resourceType": "Questionnaire",
        "status": "active",
        "launchContext": [
            {
                "name": "LaunchPatient",
                "type": "Patient",
            },
        ],
        "item": [
            {
                "type": "string",
                "linkId": "patientId",
                "initialExpression": {
                    "language": "text/fhirpath",
                    "expression": "%LaunchPatient.id",
                },
            },
        ],
    }

    launch_patient = {"resourceType": "Patient", "id": "patient-id"}

    p = await aidbox_client.execute(
        "Questionnaire/$populate",
        data=create_parameters(Questionnaire=q, LaunchPatient=launch_patient),
    )

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": q["id"],
        "item": [
            {
                "linkId": "patientId",
                "answer": [{"value": {"string": launch_patient["id"]}}],
            }
        ],
    }


@pytest.mark.asyncio
async def test_item_context_with_repeats_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [
                {
                    "name": "LaunchPatient",
                    "type": "Patient",
                },
            ],
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
                                "expression": "given",
                            },
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

    p = await q.execute("$populate", data=create_parameters(LaunchPatient=launch_patient))

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "firstName",
                        "answer": [
                            {"value": {"string": "Peter"}},
                            {"value": {"string": "Middlename"}},
                            {"value": {"string": "Pit"}},
                            {"value": {"string": "Little Pitty"}},
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
async def test_item_context_with_repeating_group_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [
                {
                    "name": "LaunchPatient",
                    "type": "Patient",
                },
            ],
            "item": [
                {
                    "type": "group",
                    "linkId": "addresses",
                    "repeats": True,
                    "itemContext": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.address",
                    },
                    "item": [
                        {
                            "type": "string",
                            "linkId": "city",
                            "initialExpression": {
                                "language": "text/fhirpath",
                                "expression": "city.first()",
                            },
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

    p = await q.execute("$populate", data=create_parameters(LaunchPatient=launch_patient))

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "city",
                        "answer": [
                            {"value": {"string": "San Francisco"}},
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
                            {"value": {"string": "San Diego"}},
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
async def test_item_context_without_repeats_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [
                {
                    "name": "LaunchPatient",
                    "type": "Patient",
                },
            ],
            "item": [
                {
                    "text": "Address",
                    "type": "group",
                    "linkId": "address",
                    "itemContext": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.address",
                    },
                    "item": [
                        {
                            "text": "City",
                            "linkId": "city",
                            "type": "string",
                            "initialExpression": {
                                "language": "text/fhirpath",
                                "expression": "city",
                            },
                        },
                        {
                            "text": "Line 1",
                            "linkId": "line-1",
                            "type": "string",
                            "initialExpression": {
                                "language": "text/fhirpath",
                                "expression": "line[0]",
                            },
                        },
                        {
                            "text": "Line 2",
                            "linkId": "line-2",
                            "type": "string",
                            "initialExpression": {
                                "language": "text/fhirpath",
                                "expression": "line[1]",
                            },
                        },
                        {
                            "text": "Country",
                            "linkId": "Country",
                            "type": "string",
                            "initialExpression": {
                                "language": "text/fhirpath",
                                "expression": "country",
                            },
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

    p = await q.execute("$populate", data=create_parameters(LaunchPatient=launch_patient))

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "answer": [{"value": {"string": "Sydney"}}],
                        "linkId": "city",
                        "text": "City",
                    },
                    {
                        "answer": [{"value": {"string": "Central park"}}],
                        "linkId": "line-1",
                        "text": "Line 1",
                    },
                    {
                        "answer": [{"value": {"string": "near metro station " "museum"}}],
                        "linkId": "line-2",
                        "text": "Line 2",
                    },
                    {
                        "answer": [{"value": {"string": "Australia"}}],
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
async def test_source_queries_populate(aidbox_client, safe_db):
    p = aidbox_client.resource("Patient")
    await p.save()

    a = aidbox_client.resource(
        "Appointment",
        **{
            "status": "booked",
            "start": "2020-01-01T00:00",
            "participant": [{"status": "accepted", "actor": p}],
        },
    )
    await a.save()

    q = aidbox_client.resource(
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
            "launchContext": [
                {
                    "name": "LaunchPatient",
                    "type": "Patient",
                },
            ],
            "sourceQueries": [
                {"localRef": "Bundle#PrePopQuery"},
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
                "answer": [{"value": {"string": a["start"]}}],
            }
        ],
    }


@pytest.mark.asyncio
async def test_multiple_answers_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [
                {
                    "name": "Diet",
                    "type": "Bundle",
                },
            ],
            "item": [
                {
                    "type": "choice",
                    "linkId": "diet",
                    "repeats": True,
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Diet.entry.resource.oralDiet.type.coding.where(system = 'http://snomed.info/sct')",
                    },
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
                        "value": {
                            "Coding": {
                                "system": "http://snomed.info/sct",
                                "code": "160671006",
                            }
                        }
                    },
                    {
                        "value": {
                            "Coding": {
                                "system": "http://snomed.info/sct",
                                "code": "302320003",
                            }
                        }
                    },
                ],
            }
        ],
    }


@pytest.mark.asyncio
async def test_fhirpath_failure_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientName",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] & ' ' & %Patient.name.family",
                    },
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
        await q.execute("$populate", data=create_parameters(LaunchPatient=launch_patient))
    except Exception as e:
        assert json.loads(str(e)) == {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "fatal",
                    "code": "invalid",
                    "diagnostics": 'Error: "%Patient.name.given[0] & \' \' & %Patient.name.family" - can only concatenate list (not "str") to list',
                }
            ],
            "text": {
                "status": "generated",
                "div": 'Error: "%Patient.name.given[0] & \' \' & %Patient.name.family" - can only concatenate list (not "str") to list',
            },
        }
        return
    assert False


@pytest.mark.asyncio
async def test_fhirpath_success_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "launchContext": [{"name": "LaunchPatient", "type": "Patient"}],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientName",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
                    },
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

    p = await q.execute("$populate", data=create_parameters(LaunchPatient=launch_patient))

    assert p == {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": q.id,
        "item": [{"linkId": "patientName"}],
    }
