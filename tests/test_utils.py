import pytest

from app.sdc.utils import (
    prepare_bundle,
    prepare_link_ids,
    resolve_fpml_template,
    resolve_string_template,
)


def test_prepare_bundle_undefined_context():
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "/QuestionnaireResponse?subject={{%CurrentAppointmentId}}",
        }
    }

    with pytest.raises(ValueError):
        prepare_bundle(bundle_entry, {})


def test_prepare_bundle():
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "/QuestionnaireResponse?subject={{%CurrentAppointmentId}}",
        }
    }

    assert prepare_bundle(bundle_entry, {"CurrentAppointmentId": "123"}) == {
        "request": {
            "method": "GET",
            "url": "/QuestionnaireResponse?subject=123",
        }
    }


def test_prepare_bundle_encode_params():
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "/Patient?email={{%QuestionnaireResponse.repeat(item).where(linkId='email').answer.value.string}}",
        }
    }

    questionnaire_response = {
        "resourceType": "QuestionnaireResponse",
        "status": "final",
        "item": [
            {
                "linkId": "email",
                "answer": [
                    {
                        "value": {"string": "test+1@example.com"},
                    }
                ],
            }
        ],
    }

    assert prepare_bundle(bundle_entry, {"QuestionnaireResponse": questionnaire_response}) == {
        "request": {
            "method": "GET",
            "url": "/Patient?email=test%2B1%40example.com",
        }
    }


def test_multuple_var_in_one_line():
    # Ref https://github.com/beda-software/aidbox-sdc/issues/1
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "Slot?specialty={{%specialty}}&start={{%start}}&status=free",
        }
    }

    env = {
        "specialty": "394586005",  # Gynecology
        "start": "2021-01-01",
    }
    assert prepare_bundle(bundle_entry, env) == {
        "request": {
            "method": "GET",
            "url": "Slot?specialty=394586005&start=2021-01-01&status=free",
        }
    }


def test_prepare_link_ids_does_not_encode_params():
    questionnaire = {
        "resourceType": "Questionnaire",
        "status": "active",
        "assembleContext": [{"name": "prefix", "type": "string"}],
        "item": [
            {
                "linkId": "{{%prefix}}line-1",
                "type": "string",
            },
            {
                "linkId": "{{%prefix}}line-2",
                "type": "string",
                "enableWhen": [
                    {
                        "question": "{{%prefix}}line-1",
                        "operator": "exists",
                        "answer": {"boolean": True},
                    }
                ],
            },
        ],
    }

    assert prepare_link_ids(questionnaire, {"prefix": "test+"}) == {
        "assembleContext": [{"name": "prefix", "type": "string"}],
        "item": [
            {"linkId": "test+line-1", "type": "string"},
            {
                "enableWhen": [
                    {"answer": {"boolean": True}, "operator": "exists", "question": "test+line-1"}
                ],
                "linkId": "test+line-2",
                "type": "string",
            },
        ],
        "resourceType": "Questionnaire",
        "status": "active",
    }


@pytest.mark.parametrize(
    "answer_type,values,expected",
    [
        ("string", ["abc", "dfe", "htd"], "/Patient?_id=abc,dfe,htd"),
        ("number", [1, 4, 5], "/Patient?_id=1,4,5"),
        ("string", ["single-id"], "/Patient?_id=single-id"),
        ("number", [5], "/Patient?_id=5"),
    ],
)
def test_resolve_string_template(answer_type, values, expected):
    questionnaire_response = {
        "resourceType": "QuestionnaireResponse",
        "item": [
            {
                "linkId": "patients-group",
                "item": [
                    {
                        "linkId": "patients-set",
                        "answer": [{"value": {answer_type: value}} for value in values],
                    }
                ],
            }
        ],
    }
    template_input = (
        "/Patient?_id={{%QuestionnaireResponse.repeat(item).where(linkId='patients-set').answer.children()."
        + answer_type
        + "}}"
    )
    result = resolve_string_template(
        template_input, {"QuestionnaireResponse": questionnaire_response}
    )
    assert result == expected


def test_fpml():
    questionnaire_response = {
        "resourceType": "QuestionnaireResponse",
        "item": [
            {
                "linkId": "patients-group",
                "item": [
                    {
                        "linkId": "patientId",
                        "answer": [{"valueString": "1"}],
                    }
                ],
            }
        ],
    }
    template = {
        "resourceType": "Patient",
        "id": "{{ %QuestionnaireResponse.answers('patientId') }}",
    }
    result = resolve_fpml_template(template, {"QuestionnaireResponse": questionnaire_response})
    assert result == {"resourceType": "Patient", "id": "1"}
