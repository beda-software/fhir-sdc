import json

import pytest

from tests.factories import (
    JUTE_BODY_EXTENSION_SD,
    make_item_constraint_ext,
    make_jute_structure_map,
    make_launch_context_ext,
    make_questionnaire_embedded_mapper_ext,
    make_source_queries_ext,
    make_target_structure_map_ext,
)


async def save_jute_structure_map(fhir_client, structure_map_id, patient_id):
    """Aidbox refuses the jute-body extension until its StructureDefinition is registered."""
    await fhir_client.resource("StructureDefinition", **JUTE_BODY_EXTENSION_SD).save()
    sm = fhir_client.resource(
        "StructureMap", **make_jute_structure_map(structure_map_id, make_patient_bundle(patient_id))
    )
    await sm.save()
    return sm


def make_embedded_jute_mapping(patient_id):
    return {
        "resourceType": "Mapping",
        "id": f"mapping-{patient_id}",
        "body": make_patient_bundle(patient_id),
    }


def make_patient_bundle(patient_id):
    return {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"method": "PUT", "url": f"Patient/{patient_id}"},
                "resource": {"resourceType": "Patient", "id": patient_id},
            }
        ],
    }


async def extracted_patient_ids(resp):
    """The ids the mappers wrote, in mapper order."""
    [bundle] = await resp.json()
    return [entry["resource"]["id"] for entry in bundle["entry"]]


async def test_healthcheck(fhir_server_client):
    resp = await fhir_server_client.get("/healthcheck")
    assert resp.status == 200
    assert await resp.json() == {"status": "ok"}


async def test_resolve_expression(fhir_server_client):
    body = {"env": {"patient_id": "p-1"}, "expression": "/Patient?_id={{%patient_id}}"}
    resp = await fhir_server_client.post("/Questionnaire/$resolve-expression", json=body)
    assert resp.status == 200
    assert await resp.json() == "/Patient?_id=p-1"


async def test_assemble_handler(fhir_server_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
    )
    await q.save()

    resp = await fhir_server_client.get(f"/Questionnaire/{q.id}/$assemble")
    assert resp.status == 200
    result = await resp.json()
    assert "id" not in result
    assert any("assembledFrom" in e.get("url", "") for e in result.get("extension", []))


async def test_constraint_check_no_errors(fhir_server_client):
    qr = {"resourceType": "QuestionnaireResponse", "status": "completed"}
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire",
                "resource": {"resourceType": "Questionnaire", "status": "active"},
            },
            {"name": "questionnaire_response", "resource": qr},
        ],
    }

    resp = await fhir_server_client.post(
        "/QuestionnaireResponse/$constraint-check", json=parameters
    )
    assert resp.status == 200
    result = await resp.json()
    assert result["resourceType"] == "QuestionnaireResponse"


async def test_questionnaire_context(fhir_server_client):
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire",
                "resource": {
                    "resourceType": "Questionnaire",
                    "status": "active",
                    "item": [],
                },
            },
        ],
    }

    resp = await fhir_server_client.post("/Questionnaire/$context", json=parameters)
    assert resp.status == 200
    result = await resp.json()
    assert "Questionnaire" in result


async def test_extract_collection_qr(fhir_server_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
    )
    await q.save()

    qr = {
        "resourceType": "QuestionnaireResponse",
        "status": "completed",
        "questionnaire": q.id,
    }
    resp = await fhir_server_client.post("/Questionnaire/$extract", json=qr)
    assert resp.status == 200
    assert await resp.json() == []


async def test_extract_collection_parameters(fhir_server_client):
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire",
                "resource": {
                    "resourceType": "Questionnaire",
                    "status": "active",
                    "item": [],
                },
            },
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse", "status": "completed"},
            },
        ],
    }

    resp = await fhir_server_client.post("/Questionnaire/$extract", json=parameters)
    assert resp.status == 200
    assert await resp.json() == []


async def test_extract_instance_qr(fhir_server_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
    )
    await q.save()

    qr = {"resourceType": "QuestionnaireResponse", "status": "completed"}
    resp = await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=qr)
    assert resp.status == 200
    assert await resp.json() == []


async def test_extract_instance_parameters(fhir_server_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
    )
    await q.save()

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse", "status": "completed"},
            },
        ],
    }
    resp = await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=parameters)
    assert resp.status == 200
    assert await resp.json() == []


async def test_extract_instance_missing_qr_error(fhir_server_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
    )
    await q.save()

    parameters = {"resourceType": "Parameters", "parameter": []}
    resp = await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=parameters)
    assert resp.status == 422
    assert (await resp.json())["resourceType"] == "OperationOutcome"


async def test_extract_instance_bad_resource_type_error(fhir_server_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
    )
    await q.save()

    resp = await fhir_server_client.post(
        f"/Questionnaire/{q.id}/$extract",
        json={"resourceType": "Patient"},
    )
    assert resp.status == 422
    assert (await resp.json())["resourceType"] == "OperationOutcome"


async def test_populate_collection(fhir_server_client):
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire",
                "resource": {
                    "resourceType": "Questionnaire",
                    "id": "test-q",
                    "status": "active",
                    "item": [],
                },
            },
        ],
    }

    resp = await fhir_server_client.post("/Questionnaire/$populate", json=parameters)
    assert resp.status == 200
    result = await resp.json()
    assert result["resourceType"] == "QuestionnaireResponse"


@pytest.mark.parametrize(
    "parameters",
    [{"resourceType": "Parameters"}, {"resourceType": "Parameters", "parameter": []}],
)
async def test_populate_collection_without_questionnaire_parameter(fhir_server_client, parameters):
    resp = await fhir_server_client.post("/Questionnaire/$populate", json=parameters)
    assert resp.status == 422
    assert (await resp.json())["resourceType"] == "OperationOutcome"


async def test_populate_instance_unknown_questionnaire(fhir_server_client):
    resp = await fhir_server_client.post(
        "/Questionnaire/missing/$populate", json={"resourceType": "Parameters", "parameter": []}
    )
    assert resp.status == 502
    assert (await resp.json())["resourceType"] == "OperationOutcome"


async def test_populate_collection_missing_questionnaire(fhir_server_client):
    # Capital-Q "Questionnaire" with empty resource → env["Questionnaire"] = {} → falsy → 422
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "Questionnaire", "resource": {}},
        ],
    }

    resp = await fhir_server_client.post("/Questionnaire/$populate", json=parameters)
    assert resp.status == 422
    assert (await resp.json())["resourceType"] == "OperationOutcome"


async def test_populate_instance(fhir_server_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
    )
    await q.save()

    resp = await fhir_server_client.post(
        f"/Questionnaire/{q.id}/$populate",
        json={"resourceType": "Parameters", "parameter": []},
    )
    assert resp.status == 200
    result = await resp.json()
    assert result["resourceType"] == "QuestionnaireResponse"


async def test_extract_collection_with_jute_template(fhir_server_client, fhir_client, safe_db):
    await save_jute_structure_map(fhir_client, "collection-sm", "jute-extract-col")

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire",
                "resource": {
                    "resourceType": "Questionnaire",
                    "status": "active",
                    "item": [],
                    "extension": [make_target_structure_map_ext("StructureMap/collection-sm")],
                },
            },
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse", "status": "completed"},
            },
        ],
    }

    resp = await fhir_server_client.post("/Questionnaire/$extract", json=parameters)
    assert resp.status == 200
    assert await extracted_patient_ids(resp) == ["jute-extract-col"]


async def test_extract_instance_with_jute_template(fhir_server_client, fhir_client, safe_db):
    await save_jute_structure_map(fhir_client, "instance-sm", "jute-extract-inst")
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
        extension=[make_target_structure_map_ext("StructureMap/instance-sm")],
    )
    await q.save()

    qr = {"resourceType": "QuestionnaireResponse", "status": "completed"}

    resp = await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=qr)
    assert resp.status == 200
    assert await extracted_patient_ids(resp) == ["jute-extract-inst"]


async def test_extract_instance_parameters_with_launch_context(
    fhir_server_client, fhir_client, safe_db
):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
        extension=[make_launch_context_ext("LaunchPatient", "Patient")],
    )
    await q.save()

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse", "status": "completed"},
            },
            {
                "name": "LaunchPatient",
                "resource": {"resourceType": "Patient"},
            },
        ],
    }
    resp = await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=parameters)
    assert resp.status == 200
    assert await resp.json() == []


_EMBEDDED_JUTE_MAPPING = make_embedded_jute_mapping("embedded-jute-patient")


async def test_extract_collection_embedded_mapper(fhir_server_client, fhir_client, safe_db):
    """Embedded mapper via valueExpression (collection $extract) — no Mapping stored in DB."""
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire",
                "resource": {
                    "resourceType": "Questionnaire",
                    "status": "active",
                    "item": [],
                    "extension": [make_questionnaire_embedded_mapper_ext(_EMBEDDED_JUTE_MAPPING)],
                },
            },
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse", "status": "completed"},
            },
        ],
    }
    resp = await fhir_server_client.post("/Questionnaire/$extract", json=parameters)
    assert resp.status == 200
    result = await resp.json()
    assert isinstance(result, list)
    assert len(result) == 1


async def test_extract_instance_embedded_mapper(fhir_server_client, fhir_client, safe_db):
    """Embedded mapper via valueExpression (instance $extract) — no Mapping stored in DB."""
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[],
        extension=[make_questionnaire_embedded_mapper_ext(_EMBEDDED_JUTE_MAPPING)],
    )
    await q.save()

    qr = {"resourceType": "QuestionnaireResponse", "status": "completed"}
    resp = await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=qr)
    assert resp.status == 200
    result = await resp.json()
    assert isinstance(result, list)
    assert len(result) == 1


_SOURCE_QUERY_FPML_MAPPING = {
    "resourceType": "Mapping",
    "type": "FHIRPath",
    "body": {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"method": "PUT", "url": "Patient/new-patient"},
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"text": "{{ %SourceQuery.resourceType }}"}],
                },
            }
        ],
    },
}

_SOURCE_QUERY_QUESTIONNAIRE = {
    "resourceType": "Questionnaire",
    "status": "active",
    "extension": [
        make_questionnaire_embedded_mapper_ext(_SOURCE_QUERY_FPML_MAPPING),
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
}


async def extract_using_collection_endpoint(fhir_server_client, fhir_client):
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "questionnaire", "resource": _SOURCE_QUERY_QUESTIONNAIRE},
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse"},
            },
        ],
    }
    return await fhir_server_client.post("/Questionnaire/$extract", json=parameters)


async def extract_using_instance_endpoint(fhir_server_client, fhir_client):
    q = fhir_client.resource("Questionnaire", **_SOURCE_QUERY_QUESTIONNAIRE)
    await q.save()
    qr = {"resourceType": "QuestionnaireResponse"}
    return await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=qr)


@pytest.mark.parametrize(
    "extract_fn", [extract_using_collection_endpoint, extract_using_instance_endpoint]
)
async def test_extract_does_not_pass_source_queries_to_mapper(
    fhir_server_client, fhir_client, safe_db, extract_fn
):
    resp = await extract_fn(fhir_server_client, fhir_client)
    assert resp.status == 400
    assert "undefined environment variable: SourceQuery" in await resp.text()


def make_constraint_questionnaire(expression: str) -> dict:
    return {
        "resourceType": "Questionnaire",
        "status": "active",
        "extension": [
            make_item_constraint_ext(
                key="constraint",
                requirements="Constraint",
                severity="error",
                human="Constraint failed",
                expression=expression,
            )
        ],
    }


def make_questionnaire_parameters(q: dict) -> dict:
    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "questionnaire", "resource": q},
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse"},
            },
        ],
    }


async def check_constraint_using_constraint_check_endpoint(fhir_server_client, fhir_client, q):
    return await fhir_server_client.post(
        "/QuestionnaireResponse/$constraint-check", json=make_questionnaire_parameters(q)
    )


async def check_constraint_using_collection_extract_endpoint(fhir_server_client, fhir_client, q):
    return await fhir_server_client.post(
        "/Questionnaire/$extract", json=make_questionnaire_parameters(q)
    )


async def check_constraint_using_instance_extract_endpoint_with_qr(
    fhir_server_client, fhir_client, q
):
    saved_q = fhir_client.resource("Questionnaire", **q)
    await saved_q.save()
    qr = {"resourceType": "QuestionnaireResponse"}
    return await fhir_server_client.post(f"/Questionnaire/{saved_q.id}/$extract", json=qr)


async def check_constraint_using_instance_extract_endpoint_with_parameters(
    fhir_server_client, fhir_client, q
):
    saved_q = fhir_client.resource("Questionnaire", **q)
    await saved_q.save()
    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse"},
            },
        ],
    }
    return await fhir_server_client.post(f"/Questionnaire/{saved_q.id}/$extract", json=parameters)


@pytest.mark.parametrize(
    "check_constraint_fn",
    [
        check_constraint_using_constraint_check_endpoint,
        check_constraint_using_collection_extract_endpoint,
        check_constraint_using_instance_extract_endpoint_with_qr,
        check_constraint_using_instance_extract_endpoint_with_parameters,
    ],
)
async def test_constraint_check_passes_a_holding_expression(
    fhir_server_client,
    fhir_client,
    safe_db,
    check_constraint_fn,
):
    resp = await check_constraint_fn(
        fhir_server_client, fhir_client, make_constraint_questionnaire("true")
    )
    assert resp.status == 200


async def test_extract_collection_resolves_questionnaire_by_canonical_url(
    fhir_server_client, fhir_client, safe_db
):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        url="http://example.com/Questionnaire/by-url",
        item=[],
        extension=[make_questionnaire_embedded_mapper_ext(_EMBEDDED_JUTE_MAPPING)],
    )
    await q.save()

    qr = {
        "resourceType": "QuestionnaireResponse",
        "status": "completed",
        "questionnaire": q["url"],
    }
    resp = await fhir_server_client.post("/Questionnaire/$extract", json=qr)
    assert resp.status == 200
    assert len(await resp.json()) == 1


async def test_extract_refuses_a_violated_constraint_before_running_the_mappers(
    fhir_server_client, fhir_client, safe_db
):
    questionnaire = make_constraint_questionnaire("false")
    questionnaire["extension"].append(
        make_questionnaire_embedded_mapper_ext(make_embedded_jute_mapping("refused-patient"))
    )

    resp = await fhir_server_client.post(
        "/Questionnaire/$extract", json=make_questionnaire_parameters(questionnaire)
    )
    assert resp.status == 422
    assert (await resp.json())["issue"][0]["code"] == "constraint"

    written = await fhir_client.resources("Patient").search(_id="refused-patient").fetch_all()
    assert written == []


async def test_extract_runs_every_mapper_in_extension_order(
    fhir_server_client, fhir_client, safe_db
):
    await save_jute_structure_map(fhir_client, "ordered-sm", "from-structure-map")
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[],
        extension=[
            make_target_structure_map_ext("StructureMap/ordered-sm"),
            make_questionnaire_embedded_mapper_ext(make_embedded_jute_mapping("from-embedded-1")),
            make_questionnaire_embedded_mapper_ext(make_embedded_jute_mapping("from-embedded-2")),
        ],
    )
    await q.save()

    qr = {"resourceType": "QuestionnaireResponse", "status": "completed"}

    resp = await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=qr)
    assert resp.status == 200
    assert await extracted_patient_ids(resp) == [
        "from-structure-map",
        "from-embedded-1",
        "from-embedded-2",
    ]
