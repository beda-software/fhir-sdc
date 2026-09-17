import fhirpy_types_r4b as r4b
import pytest

from fhir_sdc_testkit import (
    ExtractionError,
    answer,
    fill_questionnaire_response,
    launch_context,
    raise_for_extraction_errors,
    read_populated,
)

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
PATIENT = r4b.Patient(id="patient-1")
PRACTITIONER = r4b.Practitioner(id="practitioner-1")
REJECTED = {"response": {"status": "422", "outcome": {"issue": []}}}
GERMANY = answer(valueCoding=r4b.Coding(code="DE"))


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


def test_launch_context_resource_becomes_a_context_parameter() -> None:
    parameters = launch_context({"Patient": PATIENT})
    assert parameters == build_parameters(build_context("Patient", resource=PATIENT))


def test_launch_context_reference_becomes_reference_content() -> None:
    reference = r4b.Reference(reference="Patient/patient-1")

    parameters = launch_context({"Patient": reference})
    assert parameters == build_parameters(build_context("Patient", reference=reference))


def test_launch_context_list_becomes_one_parameter_per_resource() -> None:
    parameters = launch_context({"Authors": [PATIENT, PRACTITIONER]})
    assert parameters == build_parameters(
        build_context("Authors", resource=PATIENT), build_context("Authors", resource=PRACTITIONER)
    )


def build_parameters(*parameters: r4b.ParametersParameter) -> r4b.Parameters:
    return r4b.Parameters(parameter=list(parameters))


def build_context(
    name: str, *, resource: r4b.AnyResource | None = None, reference: r4b.Reference | None = None
) -> r4b.ParametersParameter:
    content = (
        r4b.ParametersParameter(name="content", valueReference=reference)
        if reference
        else r4b.ParametersParameter(name="content", resource=resource)
    )
    return r4b.ParametersParameter(
        name="context",
        part=[r4b.ParametersParameter(name="name", valueString=name), content],
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

    response = read_populated(populated)
    assert response.status == "in-progress"


def test_populated_response_is_read_as_is() -> None:
    response = read_populated({"resourceType": "QuestionnaireResponse", "status": "in-progress"})
    assert response.status == "in-progress"


def test_rejected_entry_raises() -> None:
    extracted = [{"entry": [REJECTED]}]

    with pytest.raises(ExtractionError, match="422"):
        raise_for_extraction_errors(extracted)


def test_accepted_entries_pass() -> None:
    extracted = [
        {"entry": [{"response": {"status": "201 Created"}}, {"response": {"status": "200"}}]}
    ]

    raise_for_extraction_errors(extracted)


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


def test_operation_outcome_raises() -> None:
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "error", "code": "processing"}],
    }

    with pytest.raises(ExtractionError, match="processing"):
        raise_for_extraction_errors(outcome)


def test_unexpected_response_raises() -> None:
    with pytest.raises(ExtractionError, match="Bundle"):
        raise_for_extraction_errors({"resourceType": "Bundle", "entry": [REJECTED]})


def test_parameters_return_bundle_is_checked() -> None:
    extracted = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "return", "resource": {"resourceType": "Bundle", "entry": [REJECTED]}}
        ],
    }

    with pytest.raises(ExtractionError, match="422"):
        raise_for_extraction_errors(extracted)


def test_entries_without_a_response_are_left_alone() -> None:
    transaction = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [{"request": {"method": "POST", "url": "Patient"}}],
    }

    raise_for_extraction_errors([transaction])


def build_issues(*severities: str) -> dict[str, object]:
    return {
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "issues",
                "resource": {
                    "resourceType": "OperationOutcome",
                    "issue": [
                        {"severity": severity, "code": "processing"} for severity in severities
                    ],
                },
            }
        ],
    }


def test_error_issue_raises() -> None:
    with pytest.raises(ExtractionError, match="error"):
        raise_for_extraction_errors(build_issues("warning", "error"))


def test_warning_issues_pass() -> None:
    raise_for_extraction_errors(build_issues("warning", "information"))
