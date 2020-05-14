async def test_initial_expression_populate(sdk, populate, safe_db):
    q = sdk.client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient",},],
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
    )
    await q.save()

    assert q.id is not None

    launch_patient = {"resourceType": "Patient", "id": "patienit-id"}

    p = await populate(q.id, LaunchPatient=launch_patient)

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


async def test_item_context_with_repeats_populate(sdk, populate, safe_db):
    q = sdk.client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient",},],
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
                                "expression": "given.first()",
                            },
                        },
                    ],
                },
            ],
        }
    )
    await q.save()

    assert q.id is not None

    launch_patient = {
        "resourceType": "Patient",
        "id": "patienit-id",
        "name": [
            {"given": ["Peter"]},
            {"given": ["Pit"]},
            {"given": ["Little Pitty"]},
        ],
    }

    p = await populate(q.id, LaunchPatient=launch_patient)

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "firstName",
                        "answer": [
                            {"value": {"string": "Peter"}},
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


async def test_item_context_without_repeats_populate(sdk, populate, safe_db):
    q = sdk.client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient",},],
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
        }
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

    p = await populate(q.id, LaunchPatient=launch_patient)

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
                        "answer": [
                            {"value": {"string": "near metro station " "museum"}}
                        ],
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


async def test_source_queries_populate(sdk, populate, safe_db):
    p = sdk.client.resource("Patient")
    await p.save()

    a = sdk.client.resource(
        "Appointment",
        **{
            "status": "booked",
            "start": "2020-01-01T00:00",
            "participant": [{"status": "accepted", "actor": p}],
        }
    )
    await a.save()

    q = sdk.client.resource(
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
                {"name": "LaunchPatient", "type": "Patient",},
                {"name": "PrePopQuery", "type": "Bundle",},
            ],
            "sourceQueries": [{"localRef": "Bundle#PrePopQuery"},],
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
        }
    )

    await q.save()

    p = await populate(q.id, LaunchPatient=p)

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


async def test_multiple_answers_populate(sdk, populate, safe_db):
    q = sdk.client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [{"name": "Diet", "type": "Bundle",},],
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
        }
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
                        "type": {"coding": [{"system": "UNKNOWN", "code": "ABC",},]},
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

    p = await populate(q.id, Diet=diet)

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
