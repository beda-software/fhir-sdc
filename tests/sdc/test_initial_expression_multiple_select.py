import pytest

from tests.factories import (
    create_questionnaire,
    make_initial_expression_ext,
    make_item_population_context_ext,
    make_launch_context_ext,
    make_parameters,
)

questionnaire = {
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "edit-schedule",
    "url": "edit-schedule",
    "extension": [
        make_launch_context_ext("Schedule", "Schedule"),
    ],
    "item": [
        {
            "type": "group",
            "linkId": "time-period",
            "repeats": True,
            "extension": [
                make_item_population_context_ext(
                    "%Schedule.extension.where(url='http://example.com')"
                )
            ],
            "item": [
                {
                    "type": "choice",
                    "linkId": "day-of-the-week",
                    "repeats": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "sun",
                                "system": "http://hl7.org/fhir/ValueSet/days-of-week",
                                "display": "Sunday",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "mon",
                                "system": "http://hl7.org/fhir/ValueSet/days-of-week",
                                "display": "Monday",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "tue",
                                "system": "http://hl7.org/fhir/ValueSet/days-of-week",
                                "display": "Tuesday",
                            }
                        },
                    ],
                    "extension": [
                        make_initial_expression_ext(
                            "%Questionnaire.repeat(item).where(linkId='day-of-the-week').answerOption.valueCoding.where(code in 'sun')"
                        )
                    ],
                },
            ],
        }
    ],
}

env = {
    "Practitioner": {
        "resourceType": "Practitioner",
        "id": "p1",
    },
    "Schedule": {
        "actor": [{"reference": "Practitioner/p1"}],
        "extension": [
            {
                "url": "http://example.com",
                "valueTiming": {
                    "repeat": {
                        "dayOfWeek": ["mon", "tue"],
                    }
                },
            }
        ],
        "resourceType": "Schedule",
    },
}

expected_qr = {
    "resourceType": "QuestionnaireResponse",
    "questionnaire": questionnaire["id"],
    "item": [
        {
            "linkId": "time-period",
            "item": [
                {
                    "linkId": "day-of-the-week",
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "sun",
                                "system": "http://hl7.org/fhir/ValueSet/days-of-week",
                                "display": "Sunday",
                            }
                        }
                    ],
                },
            ],
        }
    ],
}


@pytest.mark.asyncio
async def test_initial_expression_multiple_select(fhir_client, safe_db):
    q = await create_questionnaire(fhir_client, questionnaire)
    questionnaire_response = await q.execute(
        "$populate", data=make_parameters(**env)
    )

    assert questionnaire_response == expected_qr
