import fhirpy_types_r4b as r4b
import pytest

from fhir_sdc_testkit import answer
from fhir_sdc_testkit.forms import fill_questionnaire_response, get_populated_response

QUESTIONNAIRE = r4b.Questionnaire(
    id="survey",
    status="active",
    item=[
        r4b.QuestionnaireItem(linkId="date", type="dateTime"),
        r4b.QuestionnaireItem(
            linkId="has-allergy",
            type="boolean",
            item=[r4b.QuestionnaireItem(linkId="allergy-detail", type="string")],
        ),
        r4b.QuestionnaireItem(
            linkId="address",
            type="group",
            item=[
                r4b.QuestionnaireItem(linkId="country", type="choice"),
                r4b.QuestionnaireItem(
                    linkId="postal",
                    type="group",
                    item=[r4b.QuestionnaireItem(linkId="postal-code", type="string")],
                ),
            ],
        ),
        r4b.QuestionnaireItem(
            linkId="contacts",
            type="group",
            repeats=True,
            item=[
                r4b.QuestionnaireItem(linkId="phone", type="string"),
                r4b.QuestionnaireItem(
                    linkId="phone-meta",
                    type="group",
                    item=[r4b.QuestionnaireItem(linkId="label", type="string")],
                ),
            ],
        ),
    ],
)
DATE = answer(valueDateTime="2026-09-14")
POSTAL_CODE = answer(valueString="75001")
FRANCE = answer(valueCoding=r4b.Coding(code="FR"))
PHONE = answer(valueString="+1 555 0100")
OTHER_PHONE = answer(valueString="+1 555 0111")
LABEL = answer(valueString="home")
GERMANY = answer(valueCoding=r4b.Coding(code="DE"))


def test_top_level_answer_is_added() -> None:
    response = fill_questionnaire_response(QUESTIONNAIRE, build_populated(), {"date": [DATE]})
    assert response.item == [build_item("date", value=DATE)]


def test_nested_answer_creates_its_group_chain() -> None:
    response = fill_questionnaire_response(
        QUESTIONNAIRE, build_populated(), {"postal-code": [POSTAL_CODE]}
    )
    assert response.item == [
        build_item(
            "address",
            items=[build_item("postal", items=[build_item("postal-code", value=POSTAL_CODE)])],
        )
    ]


def test_answer_joins_an_existing_populated_group() -> None:
    populated = build_populated(build_item("address", items=[build_item("country", value=FRANCE)]))

    response = fill_questionnaire_response(QUESTIONNAIRE, populated, {"postal-code": [POSTAL_CODE]})
    assert response.item == [
        build_item(
            "address",
            items=[
                build_item("country", value=FRANCE),
                build_item("postal", items=[build_item("postal-code", value=POSTAL_CODE)]),
            ],
        )
    ]


def test_answer_replaces_a_populated_one_and_keeps_the_rest() -> None:
    populated = build_populated(
        build_item("date", value=DATE),
        build_item("address", items=[build_item("country", value=FRANCE)]),
    )

    response = fill_questionnaire_response(QUESTIONNAIRE, populated, {"country": [GERMANY]})
    assert response.item == [
        build_item("date", value=DATE),
        build_item("address", items=[build_item("country", value=GERMANY)]),
    ]


def test_response_is_completed() -> None:
    response = fill_questionnaire_response(QUESTIONNAIRE, build_populated(), {})
    assert response.status == "completed"


def test_populated_response_is_left_untouched() -> None:
    populated = build_populated(build_item("address", items=[]))

    fill_questionnaire_response(QUESTIONNAIRE, populated, {"country": [GERMANY]})
    assert populated == build_populated(build_item("address", items=[]))


def test_unknown_link_id_raises() -> None:
    with pytest.raises(KeyError, match="missing"):
        fill_questionnaire_response(QUESTIONNAIRE, build_populated(), {"missing": []})


def test_item_inside_a_repeating_group_raises() -> None:
    with pytest.raises(KeyError, match="phone"):
        fill_questionnaire_response(
            QUESTIONNAIRE,
            build_populated(),
            {"phone": [answer(valueString="text")]},
        )


def test_repeating_group_answers_create_one_occurrence_each() -> None:
    response = fill_questionnaire_response(
        QUESTIONNAIRE,
        build_populated(),
        {"contacts": [{"phone": [PHONE]}, {"phone": [OTHER_PHONE]}]},
    )
    assert response.item == [
        build_item("contacts", items=[build_item("phone", value=PHONE)]),
        build_item("contacts", items=[build_item("phone", value=OTHER_PHONE)]),
    ]


def test_repeating_group_answers_fill_populated_occurrences_positionally() -> None:
    populated = build_populated(
        build_item("contacts", items=[build_item("phone", value=PHONE)]),
        build_item("contacts", items=[build_item("phone", value=PHONE)]),
    )

    response = fill_questionnaire_response(
        QUESTIONNAIRE, populated, {"contacts": [{"phone": [OTHER_PHONE]}]}
    )
    assert response.item == [
        build_item("contacts", items=[build_item("phone", value=OTHER_PHONE)]),
        build_item("contacts", items=[build_item("phone", value=PHONE)]),
    ]


def test_group_inside_a_repeating_group_is_addressed_by_link_id() -> None:
    response = fill_questionnaire_response(
        QUESTIONNAIRE, build_populated(), {"contacts": [{"label": [LABEL]}]}
    )
    assert response.item == [
        build_item(
            "contacts",
            items=[build_item("phone-meta", items=[build_item("label", value=LABEL)])],
        )
    ]


def test_link_id_outside_a_repeating_group_raises_inside_it() -> None:
    with pytest.raises(KeyError, match="repeating group 'contacts'"):
        fill_questionnaire_response(
            QUESTIONNAIRE, build_populated(), {"contacts": [{"date": [DATE]}]}
        )


def test_item_under_a_question_is_addressed_by_link_id() -> None:
    detail = answer(valueString="peanuts")

    response = fill_questionnaire_response(
        QUESTIONNAIRE, build_populated(), {"allergy-detail": [detail]}
    )
    assert response.item == [
        build_item("has-allergy", items=[build_item("allergy-detail", value=detail)])
    ]


def test_populated_parameters_are_unwrapped() -> None:
    populated = {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "response",
                "resource": {"resourceType": "QuestionnaireResponse", "status": "in-progress"},
            }
        ],
    }

    response = get_populated_response(populated)
    assert response.status == "in-progress"


def test_bare_populated_response_raises() -> None:
    with pytest.raises(ValueError, match="launch context"):
        get_populated_response({"resourceType": "QuestionnaireResponse", "status": "in-progress"})


def test_items_follow_questionnaire_order() -> None:
    response = fill_questionnaire_response(
        QUESTIONNAIRE,
        build_populated(),
        {"postal-code": [POSTAL_CODE], "date": [DATE], "country": [FRANCE]},
    )
    assert response.item == [
        build_item("date", value=DATE),
        build_item(
            "address",
            items=[
                build_item("country", value=FRANCE),
                build_item("postal", items=[build_item("postal-code", value=POSTAL_CODE)]),
            ],
        ),
    ]


def test_repeating_occurrences_keep_their_order_after_sorting() -> None:
    populated = build_populated(build_item("contacts", items=[build_item("phone", value=PHONE)]))

    response = fill_questionnaire_response(
        QUESTIONNAIRE,
        populated,
        {"date": [DATE], "contacts": [{"phone": [PHONE]}, {"phone": [OTHER_PHONE]}]},
    )
    assert response.item == [
        build_item("date", value=DATE),
        build_item("contacts", items=[build_item("phone", value=PHONE)]),
        build_item("contacts", items=[build_item("phone", value=OTHER_PHONE)]),
    ]


def build_populated(*items: r4b.QuestionnaireResponseItem) -> r4b.QuestionnaireResponse:
    return r4b.QuestionnaireResponse(status="in-progress", item=list(items))


def build_item(
    link_id: str,
    *,
    value: r4b.QuestionnaireResponseItemAnswer | None = None,
    items: list[r4b.QuestionnaireResponseItem] | None = None,
) -> r4b.QuestionnaireResponseItem:
    return r4b.QuestionnaireResponseItem(
        linkId=link_id, answer=[value] if value else None, item=items
    )
