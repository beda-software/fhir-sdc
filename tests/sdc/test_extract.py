import pytest
from fhirpy.base.lib import OperationOutcome

from app.converter.aidbox import from_first_class_extension
from app.test.utils import create_parameters


@pytest.mark.asyncio
async def test_fce_extract_without_context(aidbox_client, safe_db):
    m = aidbox_client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.children().string").0""",
                        },
                    }
                ],
            }
        },
    )

    await m.save()
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "mapping": [
                {
                    "resourceType": "Mapping",
                    "id": m.id,
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                },
            ],
        },
    )
    await q.save()

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"value": {"string": "newPatient"}}],
                }
            ],
        },
    )

    extraction = await q.execute("$extract", data=qr)

    assert len(extraction) == 1

    p = await aidbox_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"


@pytest.mark.asyncio
async def test_fce_extract_with_context(aidbox_client, safe_db):
    m = aidbox_client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.children().string").0""",
                            "name": [
                                {
                                    "text": """$ fhirpath("ContextResource.name")""",
                                }
                            ],
                        },
                    }
                ],
            }
        },
    )

    await m.save()
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "mapping": [
                {
                    "resourceType": "Mapping",
                    "id": m.id,
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                },
            ],
        },
    )
    await q.save()

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"value": {"string": "newPatient"}}],
                }
            ],
        },
    )

    context = {"resourceType": "ContextResource", "name": "Name"}
    extraction = await q.execute(
        "$extract",
        data=create_parameters(QuestionnaireResponse=qr, ContextResource=context),
    )

    assert len(extraction) == 1

    p = await aidbox_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
    assert p[0].name[0].text == "Name"


@pytest.mark.asyncio
async def test_fce_extract_using_list_endpoint_with_context(aidbox_client, safe_db):
    m = aidbox_client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.children().string").0""",
                            "name": [
                                {
                                    "text": """$ fhirpath("ContextResource.name")""",
                                }
                            ],
                        },
                    }
                ],
            }
        },
    )

    await m.save()
    q = {
        "resourceType": "Questionnaire",
        "status": "active",
        "mapping": [
            {
                "resourceType": "Mapping",
                "id": m.id,
            }
        ],
        "item": [
            {
                "type": "string",
                "linkId": "patientId",
            },
        ],
    }

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": "virtual_id",
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"value": {"string": "newPatient"}}],
                }
            ],
        },
    )
    context = {"resourceType": "ContextResource", "name": "Name"}

    extraction = await aidbox_client.execute(
        "Questionnaire/$extract",
        data=create_parameters(Questionnaire=q, QuestionnaireResponse=qr, ContextResource=context),
    )

    assert len(extraction) == 1

    p = await aidbox_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
    assert p[0].name[0].text == "Name"


@pytest.mark.asyncio
async def test_fce_extract_fails_because_of_constraint_check(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "item": [
                {
                    "type": "string",
                    "linkId": "v1",
                },
                {
                    "type": "string",
                    "linkId": "v2",
                    "itemConstraint": [
                        {
                            "key": "v1eqv2",
                            "requirements": "v2 should be the same as v1",
                            "severity": "error",
                            "human": "v2 is not equal to v1",
                            # TODO: remove not() when legacy behaviour is disabled
                            "expression": "(%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')).not()",
                        },
                    ],
                },
            ],
        },
    )
    await q.save()

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "v1",
                    "answer": [{"value": {"string": "1"}}],
                },
                {
                    "linkId": "v2",
                    "answer": [{"value": {"string": "2"}}],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome):
        await q.execute("$extract", data=qr)


@pytest.mark.asyncio
async def test_fce_extract_using_list_endpoint_fails_because_of_constraint_check(
    aidbox_client, safe_db
):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "item": [
                {
                    "type": "string",
                    "linkId": "v1",
                },
                {
                    "type": "string",
                    "linkId": "v2",
                    "itemConstraint": [
                        {
                            "key": "v1eqv2",
                            "requirements": "v2 should be the same as v1",
                            "severity": "error",
                            "human": "v2 is not equal to v1",
                            # TODO: remove not() when legacy behaviour is disabled
                            "expression": "(%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')).not()",
                        },
                    ],
                },
            ],
        },
    )
    await q.save()

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "v1",
                    "answer": [{"value": {"string": "1"}}],
                },
                {
                    "linkId": "v2",
                    "answer": [{"value": {"string": "2"}}],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome):
        await aidbox_client.execute(
            "Questionnaire/$extract",
            data=create_parameters(Questionnaire=q.serialize(), QuestionnaireResponse=qr),
        )


@pytest.mark.asyncio
async def test_fce_extract_with_fhirpathmapping(aidbox_client, safe_db):
    a = aidbox_client.resource(
        "Attribute",
        type={"resourceType": "Entity", "id": "code"},
        path=["type"],
        resource={"resourceType": "Entity", "id": "Mapping"},
    )
    await a.save()
    m = aidbox_client.resource(
        "Mapping",
        **{
            "type": "FHIRPath",
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "deceasedBoolean": False,
                            "id": """{{ QuestionnaireResponse.item.where(linkId='patientId').answer.valueString }}""",
                        },
                    }
                ],
            },
        },
    )

    await m.save()

    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "mapping": [
                {
                    "resourceType": "Mapping",
                    "id": m.id,
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                },
            ],
        },
    )
    await q.save()

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"valueString": "newPatient"}],
                }
            ],
        },
    )

    extraction = await aidbox_client.execute(f"fhir/Questionnaire/{q.id}/$extract", data=qr)

    assert len(extraction) == 1

    p = await aidbox_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"


@pytest.mark.asyncio
async def test_fhir_extract_without_context(aidbox_client, fhir_client, safe_db):
    m = aidbox_client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.valueString").0""",
                        },
                    }
                ],
            }
        },
    )

    await m.save()
    q = fhir_client.resource(
        "Questionnaire",
        **(
            await from_first_class_extension(
                {
                    "status": "active",
                    "mapping": [
                        {
                            "resourceType": "Mapping",
                            "id": m.id,
                        }
                    ],
                    "item": [
                        {
                            "type": "string",
                            "linkId": "patientId",
                        },
                    ],
                },
                aidbox_client,
            )
        ),
    )
    await q.save()

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"valueString": "newPatient"}],
                }
            ],
        },
    )

    extraction = await q.execute("$extract", data=qr)

    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"


@pytest.mark.asyncio
async def test_fhir_extract_with_context(aidbox_client, fhir_client, safe_db):
    m = aidbox_client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.valueString").0""",
                            "name": [
                                {
                                    "text": """$ fhirpath("ContextResource.name")""",
                                }
                            ],
                        },
                    }
                ],
            }
        },
    )

    await m.save()
    q = fhir_client.resource(
        "Questionnaire",
        **(
            await from_first_class_extension(
                {
                    "status": "active",
                    "mapping": [
                        {
                            "resourceType": "Mapping",
                            "id": m.id,
                        }
                    ],
                    "item": [
                        {
                            "type": "string",
                            "linkId": "patientId",
                        },
                    ],
                },
                aidbox_client,
            )
        ),
    )
    await q.save()

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"valueString": "newPatient"}],
                }
            ],
        },
    )

    context = {"resourceType": "ContextResource", "name": "Name"}
    extraction = await q.execute(
        "$extract",
        data=create_parameters(QuestionnaireResponse=qr, ContextResource=context),
    )

    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
    assert p[0].name[0].text == "Name"


@pytest.mark.asyncio
async def test_fhir_extract_using_list_endpoint_with_context(aidbox_client, fhir_client, safe_db):
    m = aidbox_client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.valueString").0""",
                            "name": [
                                {
                                    "text": """$ fhirpath("ContextResource.name")""",
                                }
                            ],
                        },
                    }
                ],
            }
        },
    )

    await m.save()
    q = await from_first_class_extension(
        {
            "resourceType": "Questionnaire",
            "status": "active",
            "mapping": [
                {
                    "resourceType": "Mapping",
                    "id": m.id,
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                },
            ],
        },
        aidbox_client,
    )

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": "virtual_id",
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"valueString": "newPatient"}],
                }
            ],
        },
    )
    context = {"resourceType": "ContextResource", "name": "Name"}

    extraction = await fhir_client.execute(
        "Questionnaire/$extract",
        data=create_parameters(Questionnaire=q, QuestionnaireResponse=qr, ContextResource=context),
    )

    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
    assert p[0].name[0].text == "Name"


@pytest.mark.asyncio
async def test_fhir_extract_fails_because_of_constraint_check(aidbox_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **(
            await from_first_class_extension(
                {
                    "status": "active",
                    "item": [
                        {
                            "type": "string",
                            "linkId": "v1",
                        },
                        {
                            "type": "string",
                            "linkId": "v2",
                            "itemConstraint": [
                                {
                                    "key": "v1eqv2",
                                    "requirements": "v2 should be the same as v1",
                                    "severity": "error",
                                    "human": "v2 is not equal to v1",
                                    # TODO: remove not() when legacy behaviour is disabled
                                    "expression": "(%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')).not()",
                                },
                            ],
                        },
                    ],
                },
                aidbox_client,
            )
        ),
    )
    await q.save()

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "v1",
                    "answer": [{"value": {"string": "1"}}],
                },
                {
                    "linkId": "v2",
                    "answer": [{"value": {"string": "2"}}],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome):
        await q.execute("$extract", data=qr)


@pytest.mark.asyncio
async def test_fhir_extract_using_list_endpoint_fails_because_of_constraint_check_list(
    aidbox_client, fhir_client, safe_db
):
    q = fhir_client.resource(
        "Questionnaire",
        **(
            await from_first_class_extension(
                {
                    "status": "active",
                    "item": [
                        {
                            "type": "string",
                            "linkId": "v1",
                        },
                        {
                            "type": "string",
                            "linkId": "v2",
                            "itemConstraint": [
                                {
                                    "key": "v1eqv2",
                                    "requirements": "v2 should be the same as v1",
                                    "severity": "error",
                                    "human": "v2 is not equal to v1",
                                    # TODO: remove not() when legacy behaviour is disabled
                                    "expression": "(%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')).not()",
                                },
                            ],
                        },
                    ],
                },
                aidbox_client,
            )
        ),
    )
    await q.save()

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "v1",
                    "answer": [{"value": {"string": "1"}}],
                },
                {
                    "linkId": "v2",
                    "answer": [{"value": {"string": "2"}}],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome):
        await fhir_client.execute(
            "Questionnaire/$extract",
            data=create_parameters(Questionnaire=q.serialize(), QuestionnaireResponse=qr),
        )


PATINET_1_ID = "patient1"
PATINET_1_FULL_URL = "urn:multiple-mappers-test-patient"
PATINET_2_ID = "patient2"
OBSERVATION_CODE = "obs1"

PATIENT_BUNDLE_DATA = {
    "body": {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"url": "/Patient", "method": "POST"},
                "fullUrl": PATINET_1_FULL_URL,
                "resource": {
                    "resourceType": "Patient",
                    "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.children().string").0""",
                },
            }
        ],
    }
}

PATIENT_WITH_DUPLICATED_FULL_URL_DATA = {
    "body": {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"url": "/Patient", "method": "POST"},
                "fullUrl": PATINET_1_FULL_URL,
                "resource": {
                    "resourceType": "Patient",
                    "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId2').answer.children().string").0""",
                },
            }
        ],
    }
}

OBSERVATION_BUNDLE_DATA = {
    "body": {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"url": "/Observation", "method": "POST"},
                "resource": {
                    "resourceType": "Observation",
                    "code": {
                        "coding": [
                            {
                                "code": """$ fhirpath("QuestionnaireResponse.item.where(linkId='observationCode').answer.children().string").0"""
                            }
                        ]
                    },
                    "status": "final",
                },
            }
        ],
    }
}

OBSERVATION_WITH_ERROR_DATA = {
    "body": {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"url": "/Observation", "method": "POST"},
                "resource": {
                    "resourceType": "Observation",
                    # Wrong data to test that multiple mappers extract is atomic
                    "code": """$ fhirpath("QuestionnaireResponse.item.where(linkId='observationCode').answer.children().string").0""",
                    "status": "final",
                },
            }
        ],
    }
}

OBSERVATION_WITH_SUBJECT_DATA = {
    "body": {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"url": "/Observation", "method": "POST"},
                "resource": {
                    "resourceType": "Observation",
                    "code": {
                        "coding": [
                            {
                                "code": """$ fhirpath("QuestionnaireResponse.item.where(linkId='observationCode').answer.children().string").0"""
                            }
                        ]
                    },
                    "subject": {"uri": PATINET_1_FULL_URL},
                    "status": "final",
                },
            }
        ],
    }
}


@pytest.mark.asyncio
async def test_fce_extract_multiple_mappers(aidbox_client, safe_db):
    m1 = aidbox_client.resource(
        "Mapping",
        **PATIENT_BUNDLE_DATA,
    )

    m2 = aidbox_client.resource(
        "Mapping",
        **OBSERVATION_BUNDLE_DATA,
    )

    await m1.save()
    await m2.save()

    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "mapping": [
                {"resourceType": "Mapping", "id": m1.id},
                {"resourceType": "Mapping", "id": m2.id},
            ],
            "item": [
                {"type": "string", "linkId": "patientId"},
                {"type": "string", "linkId": "observationCode"},
            ],
        },
    )
    await q.save()

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {"linkId": "patientId", "answer": [{"value": {"string": PATINET_1_ID}}]},
                {"linkId": "observationCode", "answer": [{"value": {"string": OBSERVATION_CODE}}]},
            ],
        },
    )

    extraction = await q.execute("$extract", data=qr)

    assert extraction[0]["resourceType"] == "Bundle"
    assert len(extraction[0]["entry"]) == 2

    p = await aidbox_client.resources("Patient").search(id=PATINET_1_ID).fetch_all()
    o = await aidbox_client.resources("Observation").search(code=OBSERVATION_CODE).fetch_all()

    assert len(p) == 1
    assert len(o) == 1

    assert p[0].id == PATINET_1_ID
    assert o[0].code["coding"][0]["code"] == OBSERVATION_CODE
    assert o[0].status == "final"


@pytest.mark.asyncio
async def test_fce_extract_multiple_mappers_is_atomic(aidbox_client, safe_db):
    m1 = aidbox_client.resource(
        "Mapping",
        **PATIENT_BUNDLE_DATA,
    )

    m2 = aidbox_client.resource(
        "Mapping",
        **OBSERVATION_WITH_ERROR_DATA,
    )

    await m1.save()
    await m2.save()

    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "mapping": [
                {"resourceType": "Mapping", "id": m1.id},
                {"resourceType": "Mapping", "id": m2.id},
            ],
            "item": [
                {"type": "string", "linkId": "patientId"},
                {"type": "string", "linkId": "observationCode"},
            ],
        },
    )
    await q.save()

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {"linkId": "patientId", "answer": [{"value": {"string": PATINET_1_ID}}]},
                {"linkId": "observationCode", "answer": [{"value": {"string": OBSERVATION_CODE}}]},
            ],
        },
    )

    with pytest.raises(OperationOutcome):
        await q.execute("$extract", data=qr)

    p = await aidbox_client.resources("Patient").search(id=PATINET_1_ID).fetch_all()
    o = await aidbox_client.resources("Observation").search(code=OBSERVATION_CODE).fetch_all()

    assert p == []
    assert o == []


@pytest.mark.asyncio
async def test_fce_extract_multiple_mappers_checks_unique_full_urls(aidbox_client, safe_db):
    m1 = aidbox_client.resource(
        "Mapping",
        **PATIENT_BUNDLE_DATA,
    )

    m2 = aidbox_client.resource(
        "Mapping",
        **PATIENT_WITH_DUPLICATED_FULL_URL_DATA,
    )

    m3 = aidbox_client.resource(
        "Mapping",
        **OBSERVATION_WITH_SUBJECT_DATA,
    )

    await m1.save()
    await m2.save()
    await m3.save()

    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "mapping": [
                {"resourceType": "Mapping", "id": m1.id},
                {"resourceType": "Mapping", "id": m2.id},
                {"resourceType": "Mapping", "id": m3.id},
            ],
            "item": [
                {"type": "string", "linkId": "patientId"},
                {"type": "string", "linkId": "patientId2"},
                {"type": "string", "linkId": "observationCode"},
            ],
        },
    )
    await q.save()

    qr = aidbox_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {"linkId": "patientId", "answer": [{"value": {"string": PATINET_1_ID}}]},
                {"linkId": "patientId2", "answer": [{"value": {"string": PATINET_2_ID}}]},
                {"linkId": "observationCode", "answer": [{"value": {"string": OBSERVATION_CODE}}]},
            ],
        },
    )

    with pytest.raises(OperationOutcome):
        await q.execute("$extract", data=qr)

    p1 = await aidbox_client.resources("Patient").search(id=PATINET_1_ID).fetch_all()
    p2 = await aidbox_client.resources("Patient").search(id=PATINET_2_ID).fetch_all()
    o = await aidbox_client.resources("Observation").search(code=OBSERVATION_CODE).fetch_all()

    assert p1 == []
    assert p2 == []
    assert o == []
