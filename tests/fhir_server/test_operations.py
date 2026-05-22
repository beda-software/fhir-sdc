import json
from unittest.mock import AsyncMock, MagicMock, patch

from tests.factories import make_launch_context_ext, make_target_structure_map_ext


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
    assert any(
        "assembledFrom" in e.get("url", "") for e in result.get("extension", [])
    )


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
    template_str = json.dumps({
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"method": "PUT", "url": "Patient/jute-extract-col"},
                "resource": {"resourceType": "Patient", "id": "jute-extract-col"},
            }
        ],
    })
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

    template_str = json.dumps({
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "request": {"method": "PUT", "url": "Patient/jute-extract-inst"},
                "resource": {"resourceType": "Patient", "id": "jute-extract-inst"},
            }
        ],
    })
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
