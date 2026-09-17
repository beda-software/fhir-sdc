import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.factories import (
    get_parameter_resource,
    make_item_constraint_ext,
    make_launch_context_ext,
    make_questionnaire_embedded_mapper_ext,
    make_sdc_extract_parameters,
    make_source_queries_ext,
    make_target_structure_map_ext,
)


def _make_fake_structure_map(template_str):
    """Return a mock fhirpy resource whose get_by_path returns template_str."""
    fake_sm = MagicMock()
    fake_sm.get_by_path.return_value = template_str
    mock_sm_set = MagicMock()
    mock_sm_set.search.return_value.get = AsyncMock(return_value=fake_sm)
    return mock_sm_set


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
    assert resp.status == 500


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
    assert resp.status == 500


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
    result = await resp.json()
    assert result["error"] == "bad_request"


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
    # entry must be non-empty; Aidbox rejects Bundle.entry: []
    template_str = json.dumps(
        {
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": [
                {
                    "request": {"method": "PUT", "url": "Patient/jute-extract-col"},
                    "resource": {"resourceType": "Patient", "id": "jute-extract-col"},
                }
            ],
        }
    )
    mock_sm_set = _make_fake_structure_map(template_str)

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "questionnaire",
                "resource": {
                    "resourceType": "Questionnaire",
                    "status": "active",
                    "item": [],
                    "extension": [make_target_structure_map_ext("StructureMap/fake-sm")],
                },
            },
            {
                "name": "questionnaire_response",
                "resource": {"resourceType": "QuestionnaireResponse", "status": "completed"},
            },
        ],
    }

    with patch.object(fhir_client, "resources", return_value=mock_sm_set):
        resp = await fhir_server_client.post("/Questionnaire/$extract", json=parameters)

    assert resp.status == 200
    result = await resp.json()
    assert isinstance(result, list)
    assert len(result) == 1


async def test_extract_instance_with_jute_template(fhir_server_client, fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[{"linkId": "q1", "type": "display"}],
        extension=[make_target_structure_map_ext("StructureMap/fake-sm")],
    )
    await q.save()

    template_str = json.dumps(
        {
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": [
                {
                    "request": {"method": "PUT", "url": "Patient/jute-extract-inst"},
                    "resource": {"resourceType": "Patient", "id": "jute-extract-inst"},
                }
            ],
        }
    )
    mock_sm_set = _make_fake_structure_map(template_str)
    original_resources = fhir_client.resources

    def selective_resources(resource_type):
        if resource_type == "StructureMap":
            return mock_sm_set
        return original_resources(resource_type)

    qr = {"resourceType": "QuestionnaireResponse", "status": "completed"}
    with patch.object(fhir_client, "resources", side_effect=selective_resources):
        resp = await fhir_server_client.post(f"/Questionnaire/{q.id}/$extract", json=qr)

    assert resp.status == 200
    result = await resp.json()
    assert isinstance(result, list)
    assert len(result) == 1


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


_EMBEDDED_JUTE_MAPPING = {
    "resourceType": "Mapping",
    "id": "embedded-jute-test",
    "body": {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"method": "PUT", "url": "Patient/embedded-jute-patient"},
                "resource": {"resourceType": "Patient", "id": "embedded-jute-patient"},
            }
        ],
    },
}


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
async def test_extract_passes_source_queries_to_mapper_in_legacy_behavior(
    fhir_server_client, fhir_client, safe_db, monkeypatch, extract_fn
):
    monkeypatch.setattr(
        fhir_server_client.server.app["settings"], "EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR", True
    )

    resp = await extract_fn(fhir_server_client, fhir_client)
    assert resp.status == 200

    p = await fhir_client.resources("Patient").search(_id="new-patient").get()
    assert p.get_by_path(["name", 0, "text"]) == "Bundle"


@pytest.mark.parametrize(
    "extract_fn", [extract_using_collection_endpoint, extract_using_instance_endpoint]
)
async def test_extract_does_not_pass_source_queries_to_mapper(
    fhir_server_client, fhir_client, safe_db, monkeypatch, extract_fn
):
    monkeypatch.setattr(
        fhir_server_client.server.app["settings"], "EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR", False
    )

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
@pytest.mark.parametrize(
    ("legacy_behavior", "passing_expression"), [(True, "false"), (False, "true")]
)
async def test_constraint_check_respects_legacy_behavior(
    fhir_server_client,
    fhir_client,
    safe_db,
    monkeypatch,
    check_constraint_fn,
    legacy_behavior,
    passing_expression,
):
    monkeypatch.setattr(
        fhir_server_client.server.app["settings"], "CONSTRAINT_LEGACY_BEHAVIOR", legacy_behavior
    )

    resp = await check_constraint_fn(
        fhir_server_client, fhir_client, make_constraint_questionnaire(passing_expression)
    )
    assert resp.status == 200


async def test_questionnaire_response_extract_returns_the_bundle_to_submit(
    fhir_server_client, fhir_client, safe_db
):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[],
        extension=[make_questionnaire_embedded_mapper_ext(_EMBEDDED_JUTE_MAPPING)],
    )
    await q.save()
    qr = {"resourceType": "QuestionnaireResponse", "status": "completed", "questionnaire": q.id}

    resp = await fhir_server_client.post(
        "/QuestionnaireResponse/$extract", json=make_sdc_extract_parameters(qr)
    )
    assert resp.status == 200

    return_bundle = get_parameter_resource(await resp.json(), "return")
    assert [entry["request"]["url"] for entry in return_bundle["entry"]] == [
        "Patient/embedded-jute-patient"
    ]
    assert await fhir_client.resources("Patient").search(_id="embedded-jute-patient").fetch() == []


async def test_stored_questionnaire_response_extract_returns_the_bundle_to_submit(
    fhir_server_client, fhir_client, safe_db
):
    q = fhir_client.resource(
        "Questionnaire",
        status="active",
        item=[],
        extension=[make_questionnaire_embedded_mapper_ext(_EMBEDDED_JUTE_MAPPING)],
    )
    await q.save()
    qr = fhir_client.resource("QuestionnaireResponse", status="completed", questionnaire=q.id)
    await qr.save()

    resp = await fhir_server_client.post(f"/QuestionnaireResponse/{qr.id}/$extract")
    assert resp.status == 200
    assert len(get_parameter_resource(await resp.json(), "return")["entry"]) == 1


async def test_questionnaire_response_extract_reports_nothing_to_extract(
    fhir_server_client, fhir_client, safe_db
):
    q = fhir_client.resource("Questionnaire", status="active", item=[])
    await q.save()
    qr = {"resourceType": "QuestionnaireResponse", "status": "completed", "questionnaire": q.id}

    resp = await fhir_server_client.post(
        "/QuestionnaireResponse/$extract", json=make_sdc_extract_parameters(qr)
    )
    result = await resp.json()
    assert get_parameter_resource(result, "return") is None
    assert get_parameter_resource(result, "issues")["issue"][0]["severity"] == "information"


async def test_questionnaire_response_extract_requires_the_response(fhir_server_client):
    resp = await fhir_server_client.post(
        "/QuestionnaireResponse/$extract", json={"resourceType": "Parameters", "parameter": []}
    )
    assert resp.status == 500
