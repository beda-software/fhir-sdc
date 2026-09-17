import pytest
from fhirpy.base.exceptions import OperationOutcome
from fhirpy.base.utils import get_by_path

from app.aidbox.settings import settings
from tests.factories import (
    create_questionnaire,
    get_parameter_resource,
    make_item_constraint_ext,
    make_launch_context_ext,
    make_parameters,
    make_questionnaire_mapper_ext,
    make_sdc_extract_parameters,
    make_source_queries_ext,
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

    extraction = await fhir_client.execute(f"fhir/Questionnaire/{q.id}/$extract", data=qr)

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
        data=make_parameters(Questionnaire=q, QuestionnaireResponse=qr, ContextResource=context),
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
                                expression="(%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')).not()",
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
                                expression="(%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')).not()",
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
    o = await fhir_client.resources("Observation").search(code=OBSERVATION_CODE).fetch_all()

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
    o = await fhir_client.resources("Observation").search(code=OBSERVATION_CODE).fetch_all()

    assert p == []
    assert o == []


@pytest.mark.asyncio
async def test_fce_extract_multiple_mappers_checks_unique_full_urls(fhir_client, safe_db):
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

    assert get_by_path(excinfo.value.resource, ["issue", 0, "code"]) == "duplicate-full-url"

    p1 = await fhir_client.resources("Patient").search(id=PATIENT_1_ID).fetch_all()
    p2 = await fhir_client.resources("Patient").search(id=PATIENT_2_ID).fetch_all()
    o = await fhir_client.resources("Observation").search(code=OBSERVATION_CODE).fetch_all()

    assert p1 == []
    assert p2 == []
    assert o == []


async def create_source_query_questionnaire(fhir_client):
    m = fhir_client.resource(
        "Mapping",
        type="FHIRPath",
        body={
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": [
                {
                    "request": {"url": "/Patient/new-patient", "method": "PUT"},
                    "resource": {
                        "resourceType": "Patient",
                        "name": [{"text": "{{ %SourceQuery.resourceType }}"}],
                    },
                }
            ],
        },
    )
    await m.save()

    return await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_questionnaire_mapper_ext(m.id),
                make_source_queries_ext("#SourceQuery"),
            ],
            "contained": [
                {
                    "resourceType": "Bundle",
                    "id": "SourceQuery",
                    "type": "batch",
                    "entry": [{"request": {"method": "GET", "url": "/Patient?_count=0"}}],
                }
            ],
        },
    )


async def extract_using_instance_endpoint(fhir_client, q):
    await q.execute("$extract", data={"resourceType": "QuestionnaireResponse"})


async def extract_using_list_endpoint(fhir_client, q):
    await fhir_client.execute(
        "Questionnaire/$extract",
        data=make_parameters(
            Questionnaire=q, QuestionnaireResponse={"resourceType": "QuestionnaireResponse"}
        ),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "extract_fn", [extract_using_instance_endpoint, extract_using_list_endpoint]
)
async def test_extract_passes_source_queries_to_mapper_in_legacy_behavior(
    fhir_client, safe_db, monkeypatch, extract_fn
):
    monkeypatch.setattr(settings, "EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR", True)
    q = await create_source_query_questionnaire(fhir_client)

    await extract_fn(fhir_client, q)

    p = await fhir_client.resources("Patient").search(_id="new-patient").get()
    assert p.get_by_path(["name", 0, "text"]) == "Bundle"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "extract_fn", [extract_using_instance_endpoint, extract_using_list_endpoint]
)
async def test_extract_does_not_pass_source_queries_to_mapper(
    fhir_client, safe_db, monkeypatch, extract_fn
):
    monkeypatch.setattr(settings, "EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR", False)
    q = await create_source_query_questionnaire(fhir_client)

    with pytest.raises(OperationOutcome, match="undefined environment variable: SourceQuery"):
        await extract_fn(fhir_client, q)


@pytest.mark.asyncio
async def test_extract_resolves_questionnaire_by_canonical_url(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        url="http://example.com/Questionnaire/by-url",
        version="1.0",
        item=[{"type": "string", "linkId": "patientId"}],
        extension=[make_questionnaire_mapper_ext((await _create_patient_mapping(fhir_client)).id)],
    )
    await q.save()

    qr = {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": f"{q['url']}|1.0",
        "item": [{"linkId": "patientId", "answer": [{"valueString": PATIENT_1_ID}]}],
    }
    extraction = await fhir_client.execute("Questionnaire/$extract", data=qr)
    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search(id=PATIENT_1_ID).fetch_all()
    assert len(p) == 1


async def _create_patient_mapping(fhir_client):
    mapping = fhir_client.resource("Mapping", **PATIENT_BUNDLE_DATA)
    await mapping.save()
    return mapping


async def create_patient_questionnaire(fhir_client):
    mapping = fhir_client.resource(
        "Mapping",
        type="FHIRPath",
        body={
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": [
                {
                    "request": {"url": "/Patient", "method": "POST"},
                    "resource": {
                        "resourceType": "Patient",
                        "id": "{{ QuestionnaireResponse.item.where(linkId='patientId').answer.valueString }}",
                    },
                }
            ],
        },
    )
    await mapping.save()

    return await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_questionnaire_mapper_ext(mapping.id)],
            "item": [{"type": "string", "linkId": "patientId"}],
        },
    )


def make_patient_questionnaire_response(questionnaire_id):
    return {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": questionnaire_id,
        "item": [{"linkId": "patientId", "answer": [{"valueString": "newPatient"}]}],
    }


@pytest.mark.asyncio
async def test_extract_collection_questionnaire_response_body(fhir_client, safe_db):
    q = await create_patient_questionnaire(fhir_client)

    extraction = await fhir_client.execute(
        "Questionnaire/$extract", data=make_patient_questionnaire_response(q.id)
    )
    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search(_id="newPatient").fetch_all()
    assert len(p) == 1


@pytest.mark.asyncio
async def test_extract_collection_lowercase_questionnaire_parameter(fhir_client, safe_db):
    q = await create_patient_questionnaire(fhir_client)

    extraction = await fhir_client.execute(
        "Questionnaire/$extract",
        data=make_parameters(
            questionnaire=q.serialize(),
            questionnaire_response=make_patient_questionnaire_response(q.id),
        ),
    )
    assert len(extraction) == 1

    p = await fhir_client.resources("Patient").search(_id="newPatient").fetch_all()
    assert len(p) == 1


@pytest.mark.asyncio
async def test_extract_collection_without_questionnaire_raises(fhir_client, safe_db):
    q = await create_patient_questionnaire(fhir_client)

    with pytest.raises(OperationOutcome, match="`Questionnaire` parameter is required"):
        await fhir_client.execute(
            "Questionnaire/$extract",
            data=make_parameters(questionnaire_response=make_patient_questionnaire_response(q.id)),
        )


@pytest.mark.asyncio
async def test_extract_collection_without_questionnaire_response_raises(fhir_client, safe_db):
    q = await create_patient_questionnaire(fhir_client)

    with pytest.raises(OperationOutcome, match="`QuestionnaireResponse` parameter is required"):
        await fhir_client.execute(
            "Questionnaire/$extract", data=make_parameters(questionnaire=q.serialize())
        )


@pytest.mark.asyncio
async def test_extract_validates_launch_context(fhir_client, safe_db):
    mapping = fhir_client.resource("Mapping", type="FHIRPath", body={"resourceType": "Bundle"})
    await mapping.save()
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_questionnaire_mapper_ext(mapping.id),
            ],
            "item": [{"type": "string", "linkId": "patientId"}],
        },
    )

    with pytest.raises(OperationOutcome, match="LaunchPatient"):
        await fhir_client.execute(
            "Questionnaire/$extract", data=make_patient_questionnaire_response(q.id)
        )


def make_extract_questionnaire_response(questionnaire_id):
    return {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": questionnaire_id,
        "item": [
            {"linkId": "patientId", "answer": [{"valueString": PATIENT_1_ID}]},
            {"linkId": "observationCode", "answer": [{"valueString": OBSERVATION_CODE}]},
        ],
    }


async def create_extract_questionnaire(fhir_client, *mapping_bodies):
    mappings = []
    for mapping_body in mapping_bodies:
        mapping = fhir_client.resource("Mapping", **mapping_body)
        await mapping.save()
        mappings.append(mapping)

    return await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_questionnaire_mapper_ext(m.id) for m in mappings],
            "item": [
                {"type": "string", "linkId": "patientId"},
                {"type": "string", "linkId": "observationCode"},
            ],
        },
    )


async def extract_questionnaire_response(fhir_client, parameters):
    return await fhir_client.execute("QuestionnaireResponse/$extract", data=parameters)


@pytest.mark.asyncio
async def test_questionnaire_response_extract_returns_parameters(fhir_client, safe_db):
    q = await create_extract_questionnaire(fhir_client, PATIENT_BUNDLE_DATA)

    extraction = await extract_questionnaire_response(
        fhir_client, make_sdc_extract_parameters(make_extract_questionnaire_response(q.id))
    )
    assert extraction["resourceType"] == "Parameters"
    assert get_parameter_resource(extraction, "issues") is None

    return_bundle = get_parameter_resource(extraction, "return")
    assert return_bundle["type"] == "transaction"
    assert [entry["request"]["method"] for entry in return_bundle["entry"]] == ["POST"]

    p = await fhir_client.resources("Patient").search(id=PATIENT_1_ID).fetch_all()
    assert p == []


@pytest.mark.asyncio
async def test_stored_questionnaire_response_extract_returns_parameters(fhir_client, safe_db):
    q = await create_extract_questionnaire(fhir_client, PATIENT_BUNDLE_DATA)
    response = make_extract_questionnaire_response(q.id)
    qr = fhir_client.resource(
        "QuestionnaireResponse",
        status="completed",
        questionnaire=response["questionnaire"],
        item=response["item"],
    )
    await qr.save()

    extraction = await fhir_client.execute(
        f"QuestionnaireResponse/{qr.id}/$extract", data={"resourceType": "Parameters"}
    )
    assert len(get_parameter_resource(extraction, "return")["entry"]) == 1


@pytest.mark.asyncio
async def test_questionnaire_response_extract_uses_the_given_questionnaire(fhir_client, safe_db):
    q = await create_extract_questionnaire(fhir_client, PATIENT_BUNDLE_DATA)
    qr = {**make_extract_questionnaire_response(q.id), "questionnaire": "not-stored"}

    extraction = await extract_questionnaire_response(
        fhir_client, make_sdc_extract_parameters(qr, questionnaire=q.serialize())
    )
    assert len(get_parameter_resource(extraction, "return")["entry"]) == 1


@pytest.mark.asyncio
async def test_questionnaire_response_extract_finds_the_questionnaire_by_url(fhir_client, safe_db):
    q = await create_extract_questionnaire(fhir_client, PATIENT_BUNDLE_DATA)
    q["url"] = "http://example.com/Questionnaire/extract"
    q["version"] = "1.0"
    await q.save()
    qr = {**make_extract_questionnaire_response(q.id), "questionnaire": f"{q['url']}|1.0"}

    extraction = await extract_questionnaire_response(fhir_client, make_sdc_extract_parameters(qr))
    assert len(get_parameter_resource(extraction, "return")["entry"]) == 1


@pytest.mark.asyncio
async def test_questionnaire_response_extract_merges_mappers_into_one_bundle(fhir_client, safe_db):
    q = await create_extract_questionnaire(
        fhir_client, PATIENT_BUNDLE_DATA, OBSERVATION_BUNDLE_DATA
    )

    extraction = await extract_questionnaire_response(
        fhir_client, make_sdc_extract_parameters(make_extract_questionnaire_response(q.id))
    )
    assert len(extraction["parameter"]) == 1
    assert len(get_parameter_resource(extraction, "return")["entry"]) == 2


@pytest.mark.asyncio
async def test_questionnaire_response_extract_reports_nothing_to_extract(fhir_client, safe_db):
    q = await create_extract_questionnaire(fhir_client)

    extraction = await extract_questionnaire_response(
        fhir_client, make_sdc_extract_parameters(make_extract_questionnaire_response(q.id))
    )
    assert get_parameter_resource(extraction, "return") is None
    assert get_parameter_resource(extraction, "issues")["issue"][0]["severity"] == "information"


@pytest.mark.asyncio
async def test_questionnaire_response_extract_requires_the_response(fhir_client, safe_db):
    with pytest.raises(OperationOutcome, match="questionnaire-response"):
        await extract_questionnaire_response(
            fhir_client, {"resourceType": "Parameters", "parameter": []}
        )


@pytest.mark.asyncio
async def test_questionnaire_response_extract_requires_a_questionnaire(fhir_client, safe_db):
    qr = {"resourceType": "QuestionnaireResponse", "status": "completed"}

    with pytest.raises(OperationOutcome, match="`questionnaire` is required"):
        await extract_questionnaire_response(fhir_client, make_sdc_extract_parameters(qr))


@pytest.mark.asyncio
async def test_questionnaire_response_extract_reports_an_unknown_questionnaire(
    fhir_client, safe_db
):
    qr = make_extract_questionnaire_response("http://example.com/Questionnaire/missing")

    with pytest.raises(OperationOutcome, match="is not found"):
        await extract_questionnaire_response(fhir_client, make_sdc_extract_parameters(qr))


@pytest.mark.asyncio
async def test_questionnaire_response_extract_refuses_an_ambiguous_canonical(fhir_client, safe_db):
    url = "http://example.com/Questionnaire/versioned"
    for version in ("1.0", "2.0"):
        await create_questionnaire(
            fhir_client, {"status": "active", "url": url, "version": version}
        )
    qr = make_extract_questionnaire_response(url)

    with pytest.raises(OperationOutcome, match="several versions"):
        await extract_questionnaire_response(fhir_client, make_sdc_extract_parameters(qr))


@pytest.mark.asyncio
async def test_questionnaire_response_extract_still_raises_on_constraint_check(
    fhir_client, safe_db
):
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {"type": "string", "linkId": "v1"},
                {
                    "type": "string",
                    "linkId": "v2",
                    "extension": [
                        make_item_constraint_ext(
                            key="v1eqv2",
                            requirements="v2 should be the same as v1",
                            severity="error",
                            human="v2 is not equal to v1",
                            expression="(%QuestionnaireResponse.item.where(linkId='v1') = %QuestionnaireResponse.item.where(linkId='v2')).not()",
                        )
                    ],
                },
            ],
        },
    )

    qr = {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": q.id,
        "item": [
            {"linkId": "v1", "answer": [{"valueString": "1"}]},
            {"linkId": "v2", "answer": [{"valueString": "2"}]},
        ],
    }

    with pytest.raises(OperationOutcome):
        await extract_questionnaire_response(fhir_client, make_sdc_extract_parameters(qr))
