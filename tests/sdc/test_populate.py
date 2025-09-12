import json
import pytest
from decimal import Decimal
from fhirpathpy import evaluate

from app.test.utils import create_parameters


@pytest.mark.asyncio
async def test_initial_expression_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
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
                "type": ["Patient"],
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
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
            "item": [
                {
                    "type": "group",
                    "linkId": "names",
                    "itemPopulationContext": {
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
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
            "item": [
                {
                    "type": "group",
                    "linkId": "addresses",
                    "repeats": True,
                    "itemPopulationContext": {
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
async def test_item_context_with_repeating_group_populate_from_nonlocal_context(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [
                {"name": {"code": "LaunchPatient"}, "type": ["Patient"]},
                {"name": {"code": "LaunchEncounter"}, "type": ["Encounter"]}
            ],
            "item": [
                {
                    "type": "group",
                    "linkId": "addresses",
                    "repeats": True,
                    "itemPopulationContext": {
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
                        {
                            "type": "string",
                            "repeats": True,
                            "linkId": "encounter-id",
                            "initialExpression": {
                                "language": "text/fhirpath",
                                "expression": "%LaunchEncounter.id",
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

    launch_encounter = {
        "resourceType": "Encounter",
        "id": "encounter-example"
    }

    p = await q.execute("$populate",
                        data=create_parameters(LaunchPatient=launch_patient, LaunchEncounter=launch_encounter))

    assert p == {
        "item": [
            {
                "item": [
                    {
                        "linkId": "city",
                        "answer": [
                            {"value": {"string": "San Francisco"}},
                        ],
                    },
                    {
                        "linkId": "encounter-id",
                        "answer": [
                            {"value": {"string": "encounter-example"}},
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
                    },
                    {
                        "linkId": "encounter-id",
                        "answer": [
                            {"value": {"string": "encounter-example"}},
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
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
            "item": [
                {
                    "text": "Address",
                    "type": "group",
                    "linkId": "address",
                    "itemPopulationContext": {
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
async def test_source_query_populate(aidbox_client, safe_db):
    p = aidbox_client.resource("Patient")
    await p.save()

    a = aidbox_client.resource(
        "Appointment",
        **{
            "status": "booked",
            "start": "2020-01-01T00:00:00Z",
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
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
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
            "launchContext": [{"name": {"code": "Diet"}, "type": ["Bundle"]}],
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
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientName",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name.given.toQuantity()",
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
async def test_fhirpath_success_populate(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientName",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%LaunchPatient.name.given[0] + ' ' + %LaunchPatient.name.family",
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
        "item": [{"linkId": "patientName", "answer": [{"value": {"string": "Peter Chalmers"}}]}],
    }


@pytest.mark.asyncio
async def test_fhir_fhirpath_success_populate(fhir_client, safe_db):
    q = {
        "item": [
            {
                "type": "string",
                "linkId": "patientName",
                "extension": [
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%LaunchPatient.name.given[0] + ' ' + %LaunchPatient.name.family",
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
                        },
                    },
                    {"url": "type", "valueCode": "Patient"},
                ],
            }
        ],
        "meta": {
            "profile": ["https://emr-core.beda.software/StructureDefinition/fhir-emr-questionnaire"],
        },
    }

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "name": [{"given": ["Peter", "James"], "family": "Chalmers"}],
    }

    p = await fhir_client.execute(
        "Questionnaire/$populate",
        data=create_parameters(LaunchPatient=launch_patient, Questionnaire=q),
    )

    assert p == {
        "item": [{"answer": [{"valueString": "Peter Chalmers"}], "linkId": "patientName"}],
        "questionnaire": None,
        "resourceType": "QuestionnaireResponse",
    }


@pytest.mark.asyncio
async def test_fhir_source_query_populate(fhir_client, safe_db):
    q = {
        "meta": {
            "profile": ["https://emr-core.beda.software/StructureDefinition/fhir-emr-questionnaire"],
        },
        "item": [
            {
                "type": "dateTime",
                "linkId": "deceased",
                "extension": [
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%PrePopQuery.entry.resource.entry.resource.deceasedDateTime",
                        },
                    }
                ],
            }
        ],
        "status": "active",
        "resourceType": "Questionnaire",
        "contained": [
            {
                "id": "PrePopQuery",
                "type": "batch",
                "entry": [
                    {"request": {"url": "Patient?_id={{%LaunchPatient.id}}", "method": "GET"}}
                ],
                "resourceType": "Bundle",
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
                "valueReference": {"reference": "#Bundle#PrePopQuery"},
            },
        ],
    }

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "deceasedDateTime": "2020",
    }

    patient = fhir_client.resource("Patient", **launch_patient)
    await patient.save()

    p = await fhir_client.execute(
        "Questionnaire/$populate",
        data=create_parameters(
            LaunchPatient={"resourceType": "Patient", "id": patient["id"]}, Questionnaire=q
        ),
    )

    assert p == {
        "item": [{"answer": [{"valueDateTime": "2020"}], "linkId": "deceased"}],
        "questionnaire": None,
        "resourceType": "QuestionnaireResponse",
    }


@pytest.mark.asyncio
async def test_fhir_source_query_reference_populate(fhir_client, safe_db):
    q = {
        "meta": {
            "profile": ["https://emr-core.beda.software/StructureDefinition/fhir-emr-questionnaire"],
        },
        "item": [
            {
                "type": "dateTime",
                "linkId": "deceased",
                "extension": [
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "%PrePopQuery.entry.resource.entry.resource.deceasedDateTime",
                        },
                    }
                ],
            }
        ],
        "status": "active",
        "resourceType": "Questionnaire",
        "contained": [
            {
                "id": "PrePopQuery",
                "type": "batch",
                "entry": [
                    {"request": {"url": "Patient?_id={{%LaunchPatient.id}}", "method": "GET"}}
                ],
                "resourceType": "Bundle",
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
    }

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "deceasedDateTime": "2020",
    }

    patient = fhir_client.resource("Patient", **launch_patient)
    await patient.save()

    p = await fhir_client.execute(
        "Questionnaire/$populate",
        data=create_parameters(
            LaunchPatient={"resourceType": "Patient", "id": patient["id"]}, Questionnaire=q
        ),
    )

    assert p == {
        "item": [{"answer": [{"valueDateTime": "2020"}], "linkId": "deceased"}],
        "questionnaire": None,
        "resourceType": "QuestionnaireResponse",
    }


@pytest.mark.asyncio
async def test_fhir_source_query_populate_from_api(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
            "item": [
                {
                    "type": "dateTime",
                    "linkId": "deceased",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%PrePopQuery.entry.resource.entry.resource.deceasedDateTime",
                            },
                        }
                    ],
                }
            ],
            "status": "active",
            "resourceType": "Questionnaire",
            "contained": [
                {
                    "id": "PrePopQuery",
                    "type": "batch",
                    "entry": [
                        {"request": {"url": "Patient?_id={{%LaunchPatient.id}}", "method": "GET"}}
                    ],
                    "resourceType": "Bundle",
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
        },
    )

    await q.save()

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "deceasedDateTime": "2020",
    }

    patient = fhir_client.resource("Patient", **launch_patient)
    await patient.save()

    p = await q.execute(
        "$populate",
        data=create_parameters(LaunchPatient={"resourceType": "Patient", "id": patient["id"]}),
    )

    assert p == {
        "item": [{"answer": [{"valueDateTime": "2020"}], "linkId": "deceased"}],
        "questionnaire": q.id,
        "resourceType": "QuestionnaireResponse",
    }


@pytest.mark.asyncio
async def test_fhir_source_query_reference_populate_from_api(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
            "item": [
                {
                    "type": "dateTime",
                    "linkId": "deceased",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%PrePopQuery.entry.resource.entry.resource.deceasedDateTime",
                            },
                        }
                    ],
                }
            ],
            "status": "active",
            "resourceType": "Questionnaire",
            "contained": [
                {
                    "id": "PrePopQuery",
                    "type": "batch",
                    "entry": [
                        {"request": {"url": "Patient?_id={{%LaunchPatient.id}}", "method": "GET"}}
                    ],
                    "resourceType": "Bundle",
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
                    "valueReference": {"reference": "#Bundle#PrePopQuery"},
                },
            ],
        },
    )

    await q.save()

    launch_patient = {
        "resourceType": "Patient",
        "id": "patient-id",
        "deceasedDateTime": "2020",
    }

    patient = fhir_client.resource("Patient", **launch_patient)
    await patient.save()

    p = await q.execute(
        "$populate",
        data=create_parameters(LaunchPatient={"resourceType": "Patient", "id": patient["id"]}),
    )

    assert p == {
        "item": [{"answer": [{"valueDateTime": "2020"}], "linkId": "deceased"}],
        "questionnaire": q.id,
        "resourceType": "QuestionnaireResponse",
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
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%ChargeItemDefinition.extension('charge-item-definition-price').valueQuantity",
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
                                "code": "ChargeItemDefinition",
                            },
                        },
                        {"url": "type", "valueCode": "ChargeItemDefinition"},
                    ],
                }
            ],
        },
    )

    await q.save()

    charge_item_definition = {
        "resourceType": "ChargeItemDefinition",
        "extension": [
            {
                "url": "charge-item-definition-price",
                "valueQuantity": {"code": "USD", "value": 33.3, "system": "urn:iso:std:iso:4217"},
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
async def test_source_query_with_qr_vars_populate(aidbox_client, safe_db):
    """
    It's unusual case according to FHIR SDC spec, but we use QR vars in source queries for constraint checks
    The test checks that populate does not fail when we access QR
    """

    p = aidbox_client.resource("Patient")
    await p.save()

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
                                "url": "Appointment?patient={{(%QuestionnaireResponse.item.where(linkId='patient-id').answer.valueString | 'undefined').first()}}",
                            },
                        },
                    ],
                }
            ],
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
            "sourceQueries": [{"localRef": "Bundle#PrePopQuery"}],
            "item": [
                {
                    "type": "string",
                    "linkId": "last-appointment",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%PrePopQuery.entry.resource.entry.resource.start",
                    },
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


@pytest.mark.asyncio
async def test_fhir_source_query_with_qr_vars_populate(fhir_client, safe_db):
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
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": ["Patient"]}],
            "sourceQueries": [{"localRef": "Bundle#PrePopQuery"}],
            "item": [
                {
                    "type": "string",
                    "linkId": "last-appointment",
                    "initialExpression": {
                        "language": "text/fhirpath",
                        "expression": "%PrePopQuery.entry.resource.entry.resource.start",
                    },
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
