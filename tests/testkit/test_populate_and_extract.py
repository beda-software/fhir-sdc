"""fhir-sdc-testkit against a running server: the shapes it sends and reads are the engine's."""

import fhirpy_types_r4b as r4b
import pytest
from fhirpy.base.exceptions import OperationOutcome

from fhir_sdc_testkit import (
    ExtractionError,
    answer,
    launch_context,
    populate,
    populate_and_extract,
)
from tests.factories import (
    create_mapping,
    create_questionnaire,
    make_initial_expression_ext,
    make_item_constraint_ext,
    make_launch_context_ext,
    make_questionnaire,
    make_questionnaire_mapper_ext,
)


@pytest.fixture
async def subject(typed_fhir_client, safe_db):
    patient = await typed_fhir_client.create(r4b.Patient())
    return r4b.Reference(reference=f"Patient/{patient.id}")


async def test_populated_and_typed_answers_reach_the_mapper(
    fhir_client, typed_fhir_client, subject, safe_db
):
    mapping = await create_mapping(
        fhir_client,
        build_patient_bundle(
            name=[
                {
                    "family": build_answer_template("family"),
                    "given": [build_answer_template("given")],
                }
            ]
        ),
    )
    launch_patient = await typed_fhir_client.create(
        r4b.Patient(name=[r4b.HumanName(given=["Leo"])])
    )
    questionnaire = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_questionnaire_mapper_ext(mapping.id),
            ],
            "item": [
                {
                    "linkId": "given",
                    "type": "string",
                    "extension": [make_initial_expression_ext("%LaunchPatient.name.given")],
                },
                {"linkId": "family", "type": "string"},
            ],
        },
    )

    response, _ = await populate_and_extract(
        typed_fhir_client,
        questionnaire.id,
        parameters=launch_context({"LaunchPatient": launch_patient}, subject=subject),
        answers={"family": [answer(valueString="Test")]},
        submit=True,
    )
    assert response.status == "completed"

    [created] = await typed_fhir_client.resources(r4b.Patient).search(family="Test").fetch_all()
    assert created.name[0].given == ["Leo"]


async def test_unsaved_questionnaire_is_extracted_and_nothing_is_saved(
    fhir_client, typed_fhir_client, subject, safe_db
):
    mapping = await create_mapping(
        fhir_client, build_patient_bundle(name=[{"family": build_answer_template("family")}])
    )
    questionnaire = r4b.Questionnaire.model_validate(
        make_questionnaire(
            {
                "status": "active",
                "extension": [make_questionnaire_mapper_ext(mapping.id)],
                "item": [{"linkId": "family", "type": "string"}],
            }
        )
    )

    response, bundle = await populate_and_extract(
        typed_fhir_client,
        questionnaire,
        parameters=launch_context({}, subject=subject),
        answers={"family": [answer(valueString="Test")]},
    )
    assert response.id is None
    assert [entry["resource"]["name"] for entry in bundle["entry"]] == [[{"family": "Test"}]]

    created = await typed_fhir_client.resources(r4b.Patient).search(family="Test").fetch_all()
    assert created == []


async def test_populate_returns_the_populated_response_unsaved(
    fhir_client, typed_fhir_client, subject, safe_db
):
    launch_patient = await typed_fhir_client.create(
        r4b.Patient(name=[r4b.HumanName(given=["Leo"])])
    )
    questionnaire = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_launch_context_ext("LaunchPatient", "Patient")],
            "item": [
                {
                    "linkId": "given",
                    "type": "string",
                    "extension": [make_initial_expression_ext("%LaunchPatient.name.given")],
                }
            ],
        },
    )

    populated = await populate(
        typed_fhir_client,
        questionnaire.id,
        parameters=launch_context({"LaunchPatient": launch_patient}, subject=subject),
    )
    assert populated.id is None
    assert populated.item[0].answer[0].valueString == "Leo"


async def test_questionnaire_is_found_by_canonical(
    fhir_client, typed_fhir_client, subject, safe_db
):
    url = "https://example.com/Questionnaire/intake"
    for version in ["1", "2"]:
        await create_questionnaire(
            fhir_client,
            {
                "status": "active",
                "url": url,
                "version": version,
                "item": [
                    {
                        "linkId": "version",
                        "type": "string",
                        "extension": [make_initial_expression_ext(f"'{version}'")],
                    }
                ],
            },
        )
    parameters = launch_context({}, subject=subject)

    populated = await populate(typed_fhir_client, f"{url}|2", parameters=parameters)
    assert populated.item[0].answer[0].valueString == "2"

    with pytest.raises(LookupError, match="several versions"):
        await populate(typed_fhir_client, url, parameters=parameters)

    with pytest.raises(LookupError, match="not found"):
        await populate(typed_fhir_client, f"{url}|3", parameters=parameters)


async def test_repeating_group_occurrences_are_saved(
    fhir_client, typed_fhir_client, subject, safe_db
):
    questionnaire = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "linkId": "people",
                    "type": "group",
                    "repeats": True,
                    "item": [{"linkId": "family", "type": "string"}],
                }
            ],
        },
    )

    response, _ = await populate_and_extract(
        typed_fhir_client,
        questionnaire.id,
        parameters=launch_context({}, subject=subject),
        answers={
            "people": [
                {"family": [answer(valueString="First")]},
                {"family": [answer(valueString="Second")]},
            ]
        },
        submit=True,
    )

    saved = await typed_fhir_client.get(r4b.QuestionnaireResponse, response.id)
    assert [item.item[0].answer[0].valueString for item in saved.item] == ["First", "Second"]


async def test_violated_constraint_refuses_the_submission(
    fhir_client, typed_fhir_client, subject, safe_db
):
    questionnaire = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "item": [
                {
                    "linkId": "family",
                    "type": "string",
                    "extension": [
                        make_item_constraint_ext(
                            key="family-required",
                            requirements="A family name is always recorded",
                            severity="error",
                            human="Family name is required",
                            expression=(
                                "%QuestionnaireResponse.repeat(item).where(linkId='family')"
                                ".answer.valueString.exists()"
                            ),
                        )
                    ],
                },
                {"linkId": "given", "type": "string"},
            ],
        },
    )

    with pytest.raises(OperationOutcome) as refused:
        await populate_and_extract(
            typed_fhir_client,
            questionnaire.id,
            parameters=launch_context({}, subject=subject),
            answers={"given": [answer(valueString="Leo")]},
        )
    assert refused.value.resource["issue"][0]["code"] == "family-required"


async def test_rejected_transaction_raises(fhir_client, typed_fhir_client, subject, safe_db):
    mapping = await create_mapping(
        fhir_client, build_patient_bundle(gender=build_answer_template("gender"))
    )
    questionnaire = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_questionnaire_mapper_ext(mapping.id)],
            "item": [{"linkId": "gender", "type": "string"}],
        },
    )

    with pytest.raises(OperationOutcome) as rejected:
        await populate_and_extract(
            typed_fhir_client,
            questionnaire.id,
            parameters=launch_context({}, subject=subject),
            answers={"gender": [answer(valueString="not-a-gender")]},
            submit=True,
        )
    assert rejected.value.resource["issue"][0]["code"] == "invalid"


async def test_rejected_batch_entry_raises(fhir_client, typed_fhir_client, subject, safe_db):
    mapping = await create_mapping(
        fhir_client, build_patient_bundle("batch", gender=build_answer_template("gender"))
    )
    questionnaire = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [make_questionnaire_mapper_ext(mapping.id)],
            "item": [{"linkId": "gender", "type": "string"}],
        },
    )

    with pytest.raises(ExtractionError):
        await populate_and_extract(
            typed_fhir_client,
            questionnaire.id,
            parameters=launch_context({}, subject=subject),
            answers={"gender": [answer(valueString="not-a-gender")]},
            submit=True,
        )


def build_patient_bundle(bundle_type="transaction", **patient):
    return {
        "resourceType": "Bundle",
        "type": bundle_type,
        "entry": [
            {
                "request": {"url": "/Patient", "method": "POST"},
                "resource": {"resourceType": "Patient", **patient},
            }
        ],
    }


def build_answer_template(link_id):
    return (
        f"{{{{ QuestionnaireResponse.repeat(item).where(linkId='{link_id}').answer.valueString }}}}"
    )
