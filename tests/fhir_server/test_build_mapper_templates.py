import json
from unittest.mock import AsyncMock, MagicMock

from app.fhir_server.operations import _build_mapper_templates
from app.sdc.getters import QUESTIONNAIRE_MAPPER_URL, TARGET_STRUCTURE_MAP_URL


def _mock_client_with_structure_map(template_body: dict):
    fake_sm = MagicMock()
    fake_sm.get_by_path.return_value = json.dumps(template_body)
    client = MagicMock()
    client.resources.return_value.search.return_value.get = AsyncMock(return_value=fake_sm)
    return client


_JUTE_BODY = {"resourceType": "Bundle", "type": "transaction", "entry": []}
_MAPPING_BODY = {"resourceType": "Mapping", "id": "m1", "body": {"key": "value"}}


async def test_empty_extensions():
    result = await _build_mapper_templates(MagicMock(), {"extension": []})
    assert result == []


async def test_no_extension_key():
    result = await _build_mapper_templates(MagicMock(), {})
    assert result == []


async def test_embedded_mapper_valueexpression():
    questionnaire = {
        "extension": [
            {
                "url": QUESTIONNAIRE_MAPPER_URL,
                "valueExpression": {"language": "jute", "expression": json.dumps(_MAPPING_BODY)},
            }
        ]
    }
    result = await _build_mapper_templates(MagicMock(), questionnaire)
    assert result == [_MAPPING_BODY]


async def test_embedded_mapper_fpml_valueexpression():
    fpml_body = {"resourceType": "Mapping", "id": "m2", "type": "FHIRPath", "body": {}}
    questionnaire = {
        "extension": [
            {
                "url": QUESTIONNAIRE_MAPPER_URL,
                "valueExpression": {"language": "fpml", "expression": json.dumps(fpml_body)},
            }
        ]
    }
    result = await _build_mapper_templates(MagicMock(), questionnaire)
    assert result == [fpml_body]


async def test_embedded_mapper_no_valueexpression_skipped():
    questionnaire = {
        "extension": [
            {
                "url": QUESTIONNAIRE_MAPPER_URL,
                "valueReference": {"reference": "Mapping/some-id"},
            }
        ]
    }
    result = await _build_mapper_templates(MagicMock(), questionnaire)
    assert result == []


async def test_embedded_mapper_empty_expression_skipped():
    questionnaire = {
        "extension": [
            {
                "url": QUESTIONNAIRE_MAPPER_URL,
                "valueExpression": {"language": "jute", "expression": ""},
            }
        ]
    }
    result = await _build_mapper_templates(MagicMock(), questionnaire)
    assert result == []


async def test_target_structure_map():
    client = _mock_client_with_structure_map(_JUTE_BODY)
    questionnaire = {
        "extension": [
            {
                "url": TARGET_STRUCTURE_MAP_URL,
                "valueCanonical": "StructureMap/my-sm",
            }
        ]
    }
    result = await _build_mapper_templates(client, questionnaire)
    assert result == [_JUTE_BODY]
    client.resources.assert_called_once_with("StructureMap")
    client.resources.return_value.search.assert_called_once_with(_id="my-sm")


async def test_unknown_extension_ignored():
    questionnaire = {
        "extension": [{"url": "http://example.com/some-other-extension", "valueString": "x"}]
    }
    result = await _build_mapper_templates(MagicMock(), questionnaire)
    assert result == []


async def test_mixed_extensions():
    client = _mock_client_with_structure_map(_JUTE_BODY)
    questionnaire = {
        "extension": [
            {"url": TARGET_STRUCTURE_MAP_URL, "valueCanonical": "StructureMap/sm1"},
            {
                "url": QUESTIONNAIRE_MAPPER_URL,
                "valueExpression": {"language": "jute", "expression": json.dumps(_MAPPING_BODY)},
            },
        ]
    }
    result = await _build_mapper_templates(client, questionnaire)
    assert result == [_JUTE_BODY, _MAPPING_BODY]


async def test_multiple_embedded_mappers():
    body1 = {"resourceType": "Mapping", "id": "m1", "body": {}}
    body2 = {"resourceType": "Mapping", "id": "m2", "body": {}}
    questionnaire = {
        "extension": [
            {
                "url": QUESTIONNAIRE_MAPPER_URL,
                "valueExpression": {"language": "jute", "expression": json.dumps(body1)},
            },
            {
                "url": QUESTIONNAIRE_MAPPER_URL,
                "valueExpression": {"language": "jute", "expression": json.dumps(body2)},
            },
        ]
    }
    result = await _build_mapper_templates(MagicMock(), questionnaire)
    assert result == [body1, body2]
