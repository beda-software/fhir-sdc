import json
from unittest.mock import MagicMock

from app.fhir_server.operations import _build_mapper_templates
from app.sdc.getters import QUESTIONNAIRE_MAPPER_URL


async def test_empty_extensions():
    result = await _build_mapper_templates(MagicMock(), {"extension": []})
    assert result == []


async def test_no_extension_key():
    result = await _build_mapper_templates(MagicMock(), {})
    assert result == []


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


async def test_unknown_extension_ignored():
    questionnaire = {
        "extension": [{"url": "http://example.com/some-other-extension", "valueString": "x"}]
    }
    result = await _build_mapper_templates(MagicMock(), questionnaire)
    assert result == []
