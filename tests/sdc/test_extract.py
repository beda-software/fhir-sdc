import pytest
from fhirpy.base.exceptions import OperationOutcome
from fhirpy.base.utils import get_by_path
from tests.factories import (
    create_questionnaire,
    make_parameters,
    make_questionnaire_mapper_ext,
    make_item_constraint_ext,
)


@pytest.mark.asyncio
async def test_extract_with_fhirpathmapping(fhir_client, safe_db):
    a = fhir_client.resource(
        "Attribute",
        type={"resourceType": "Entity", "id": "code"},
        path=["type"],
        resource={"resourceType": "Entity", "id": "Mapping"},
    )
    await a.save()
    m = fhir_client.resource(
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

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_questionnaire_mapper_ext(m.id)],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                },
            ],
        },
    )

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

    extraction = await fhir_client.execute(
        f"fhir/Questionnaire/{q.id}/$extract", data=qr
    )

    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"


@pytest.mark.asyncio
async def test_extract_without_context(fhir_client, safe_db):
    m = fhir_client.resource(
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
    q = await create_questionnaire(
        fhir_client,
        (
            {
                "status": "active",
                "extension": [make_questionnaire_mapper_ext(m.id)],
                "item": [
                    {
                        "type": "string",
                        "linkId": "patientId",
                    },
                ],
            }
        ),
    )

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
async def test_extract_with_context(fhir_client, safe_db):
    m = fhir_client.resource(
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
    q = await create_questionnaire(
        fhir_client,
        (
            {
                "status": "active",
                "extension": [make_questionnaire_mapper_ext(m.id)],
                "item": [
                    {
                        "type": "string",
                        "linkId": "patientId",
                    },
                ],
            }
        ),
    )

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
        data=make_parameters(QuestionnaireResponse=qr, ContextResource=context),
    )

    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
    assert p[0].name[0].text == "Name"


@pytest.mark.asyncio
async def test_extract_using_list_endpoint_with_context(fhir_client, safe_db):
    m = fhir_client.resource(
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
    q = await create_questionnaire(
        fhir_client,
        {
            "resourceType": "Questionnaire",
            "status": "active",
            "extension": [make_questionnaire_mapper_ext(m.id)],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                },
            ],
        },
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
        data=make_parameters(
            Questionnaire=q, QuestionnaireResponse=qr, ContextResource=context
        ),
    )

    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
    assert p[0].name[0].text == "Name"


@pytest.mark.asyncio
async def test_extract_fails_because_of_constraint_check(fhir_client, safe_db):
    q = await create_questionnaire(
        fhir_client,
        (
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
                        "extension": [
                            make_item_constraint_ext(
                                key="v1eqv2",
                                requirements="v2 should be the same as v1",
                                severity="error",
                                human="v2 is not equal to v1",
                                expression="%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')"
                            )
                        ],
                    },
                ],
            }
        ),
    )

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "v1",
                    "answer": [{"valueString": "1"}],
                },
                {
                    "linkId": "v2",
                    "answer": [{"valueString": "2"}],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome):
        await q.execute("$extract", data=qr)


@pytest.mark.asyncio
async def test_extract_using_list_endpoint_fails_because_of_constraint_check_list(
    fhir_client, safe_db
):
    q = await create_questionnaire(
        fhir_client,
        (
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
                        "extension": [
                            make_item_constraint_ext(
                                key="v1eqv2",
                                requirements="v2 should be the same as v1",
                                severity="error",
                                human="v2 is not equal to v1",
                                expression="%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')"
                            )
                        ],
                    },
                ],
            }
        ),
    )

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "v1",
                    "answer": [{"valueString": "1"}],
                },
                {
                    "linkId": "v2",
                    "answer": [{"valueString": "2"}],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome):
        await fhir_client.execute(
            "Questionnaire/$extract",
            data=make_parameters(Questionnaire=q.serialize(), QuestionnaireResponse=qr),
        )


PATIENT_1_ID = "patient1"
PATIENT_1_FULL_URL = "urn:multiple-mappers-test-patient"
PATIENT_2_ID = "patient2"
OBSERVATION_CODE = "obs1"

PATIENT_BUNDLE_DATA = {
    "body": {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"url": "/Patient", "method": "POST"},
                "fullUrl": PATIENT_1_FULL_URL,
                "resource": {
                    "resourceType": "Patient",
                    "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.valueString").0""",
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
                "fullUrl": PATIENT_1_FULL_URL,
                "resource": {
                    "resourceType": "Patient",
                    "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId2').answer.valueString").0""",
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
                                "code": """$ fhirpath("QuestionnaireResponse.item.where(linkId='observationCode').answer.valueString").0"""
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
                    "code": """$ fhirpath("QuestionnaireResponse.item.where(linkId='observationCode').answer.valueString").0""",
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
                                "code": """$ fhirpath("QuestionnaireResponse.item.where(linkId='observationCode').answer.valueString").0"""
                            }
                        ]
                    },
                    "subject": {"uri": PATIENT_1_FULL_URL},
                    "status": "final",
                },
            }
        ],
    }
}


@pytest.mark.asyncio
async def test_extract_multiple_mappers(fhir_client, safe_db):
    m1 = fhir_client.resource(
        "Mapping",
        **PATIENT_BUNDLE_DATA,
    )

    m2 = fhir_client.resource(
        "Mapping",
        **OBSERVATION_BUNDLE_DATA,
    )

    await m1.save()
    await m2.save()

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_questionnaire_mapper_ext(m1.id),
                make_questionnaire_mapper_ext(m2.id),
            ],
            "item": [
                {"type": "string", "linkId": "patientId"},
                {"type": "string", "linkId": "observationCode"},
            ],
        },
    )

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {"linkId": "patientId", "answer": [{"valueString": PATIENT_1_ID}]},
                {
                    "linkId": "observationCode",
                    "answer": [{"valueString": OBSERVATION_CODE}],
                },
            ],
        },
    )

    extraction = await q.execute("$extract", data=qr)

    assert extraction[0]["resourceType"] == "Bundle"
    assert len(extraction[0]["entry"]) == 2

    p = await fhir_client.resources("Patient").search(id=PATIENT_1_ID).fetch_all()
    o = (
        await fhir_client.resources("Observation")
        .search(code=OBSERVATION_CODE)
        .fetch_all()
    )

    assert len(p) == 1
    assert len(o) == 1

    assert p[0].id == PATIENT_1_ID
    assert o[0].code["coding"][0]["code"] == OBSERVATION_CODE
    assert o[0].status == "final"


@pytest.mark.asyncio
async def test_extract_multiple_mappers_is_atomic(fhir_client, safe_db):
    m1 = fhir_client.resource(
        "Mapping",
        **PATIENT_BUNDLE_DATA,
    )

    m2 = fhir_client.resource(
        "Mapping",
        **OBSERVATION_WITH_ERROR_DATA,
    )

    await m1.save()
    await m2.save()

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_questionnaire_mapper_ext(m1.id),
                make_questionnaire_mapper_ext(m2.id),
            ],
            "item": [
                {"type": "string", "linkId": "patientId"},
                {"type": "string", "linkId": "observationCode"},
            ],
        },
    )

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {"linkId": "patientId", "answer": [{"valueString": PATIENT_1_ID}]},
                {
                    "linkId": "observationCode",
                    "answer": [{"valueString": OBSERVATION_CODE}],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome) as excinfo:
        await q.execute("$extract", data=qr)

    assert get_by_path(excinfo.value.resource, ["issue", 0, "code"]) == "invalid"

    p = await fhir_client.resources("Patient").search(id=PATIENT_1_ID).fetch_all()
    o = (
        await fhir_client.resources("Observation")
        .search(code=OBSERVATION_CODE)
        .fetch_all()
    )

    assert p == []
    assert o == []


@pytest.mark.asyncio
async def test_fce_extract_multiple_mappers_checks_unique_full_urls(
    fhir_client, safe_db
):
    m1 = fhir_client.resource(
        "Mapping",
        **PATIENT_BUNDLE_DATA,
    )

    m2 = fhir_client.resource(
        "Mapping",
        **PATIENT_WITH_DUPLICATED_FULL_URL_DATA,
    )

    m3 = fhir_client.resource(
        "Mapping",
        **OBSERVATION_WITH_SUBJECT_DATA,
    )

    await m1.save()
    await m2.save()
    await m3.save()

    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_questionnaire_mapper_ext(m1.id),
                make_questionnaire_mapper_ext(m2.id),
                make_questionnaire_mapper_ext(m3.id),
            ],
            "item": [
                {"type": "string", "linkId": "patientId"},
                {"type": "string", "linkId": "patientId2"},
                {"type": "string", "linkId": "observationCode"},
            ],
        },
    )

    qr = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {"linkId": "patientId", "answer": [{"valueString": PATIENT_1_ID}]},
                {"linkId": "patientId2", "answer": [{"valueString": PATIENT_2_ID}]},
                {
                    "linkId": "observationCode",
                    "answer": [{"valueString": OBSERVATION_CODE}],
                },
            ],
        },
    )

    with pytest.raises(OperationOutcome) as excinfo:
        await q.execute("$extract", data=qr)

    assert (
        get_by_path(excinfo.value.resource, ["issue", 0, "code"])
        == "duplicate-full-url"
    )

    p1 = await fhir_client.resources("Patient").search(id=PATIENT_1_ID).fetch_all()
    p2 = await fhir_client.resources("Patient").search(id=PATIENT_2_ID).fetch_all()
    o = (
        await fhir_client.resources("Observation")
        .search(code=OBSERVATION_CODE)
        .fetch_all()
    )

    assert p1 == []
    assert p2 == []
    assert o == []
