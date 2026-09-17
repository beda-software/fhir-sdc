"""fhir-sdc-testkit against a running server: the shapes it sends and reads are the engine's."""

import fhirpy_types_r4b as r4b
import pytest
from fhirpy.base.exceptions import OperationOutcome

from app.aidbox.settings import settings
from fhir_sdc_testkit import ExtractionError, answer, launch_context, populate_and_extract
from tests.factories import (
    create_questionnaire,
    make_initial_expression_ext,
    make_item_constraint_ext,
    make_launch_context_ext,
    make_questionnaire_mapper_ext,
)


@pytest.fixture
def strict_constraints(monkeypatch):
    """A constraint expression states what must hold; the legacy behaviour this suite runs inverts it."""
    monkeypatch.setattr(settings, "CONSTRAINT_LEGACY_BEHAVIOR", False)


async def create_mapping(fhir_client, body):
    attribute = fhir_client.resource(
        "Attribute",
        type={"resourceType": "Entity", "id": "code"},
        path=["type"],
        resource={"resourceType": "Entity", "id": "Mapping"},
    )
    await attribute.save()
    mapping = fhir_client.resource("Mapping", type="FHIRPath", body=body)
    await mapping.save()
    return mapping


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


def read_answer(link_id):
    return (
        f"{{{{ QuestionnaireResponse.repeat(item).where(linkId='{link_id}').answer.valueString }}}}"
    )


async def test_populated_and_typed_answers_reach_the_mapper(
    fhir_client, typed_fhir_client, safe_db
):
    mapping = await create_mapping(
        fhir_client,
        build_patient_bundle(
            name=[{"family": read_answer("family"), "given": [read_answer("given")]}]
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

    response = await populate_and_extract(
        typed_fhir_client,
        questionnaire.id,
        parameters=launch_context({"LaunchPatient": launch_patient}),
        answers={"family": [answer(valueString="Test")]},
    )
    assert response.status == "completed"

    [created] = await typed_fhir_client.resources(r4b.Patient).search(family="Test").fetch_all()
    assert created.name[0].given == ["Leo"]


async def test_repeating_group_occurrences_are_saved(fhir_client, typed_fhir_client, safe_db):
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

    response = await populate_and_extract(
        typed_fhir_client,
        questionnaire.id,
        answers={
            "people": [
                {"family": [answer(valueString="First")]},
                {"family": [answer(valueString="Second")]},
            ]
        },
    )

    saved = await typed_fhir_client.get(r4b.QuestionnaireResponse, response.id)
    assert [item.item[0].answer[0].valueString for item in saved.item] == ["First", "Second"]


async def test_violated_constraint_refuses_the_submission(
    fhir_client, typed_fhir_client, strict_constraints, safe_db
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
            answers={"given": [answer(valueString="Leo")]},
        )
    assert refused.value.resource["issue"][0]["code"] == "family-required"


async def test_rejected_mapper_entry_raises(fhir_client, typed_fhir_client, safe_db):
    mapping = await create_mapping(
        fhir_client, build_patient_bundle("batch", gender=read_answer("gender"))
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
            answers={"gender": [answer(valueString="not-a-gender")]},
        )
