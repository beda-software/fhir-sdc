import json

import pytest

from app.converter.fhir_to_fce import to_first_class_extension
from tests.fce.resources.fce import (
    allergies_aidbox_QuestionnaireResponse,
    allergies_fhir_QuestionnaireResponse,
    allergies_inprogress_aidbox_QuestionnaireResponse,
    allergies_inprogress_fhir_QuestionnaireResponse,
    cardiology_aidbox_QuestionnaireResponse,
    cardiology_fhir_QuestionnaireResponse,
    few_answers_aidbox_questionnaire_response,
    few_answers_fhir_questionnaire_response,
    gad7_aidbox_QuestionnaireResponse,
    gad7_fhir_QuestionnaireResponse,
    immunization_aidbox_QuestionnaireResponse,
    immunization_fhir_QuestionnaireResponse,
    medication_aidbox_QuestionnaireResponse,
    medication_fhir_QuestionnaireResponse,
    newappointment_aidbox_QuestionnaireResponse,
    newappointment_fhir_QuestionnaireResponse,
    patient_aidbox_QuestionnaireResponse,
    patient_fhir_QuestionnaireResponse,
    phq2phq9_aidbox_QuestionnaireResponse,
    phq2phq9_fhir_QuestionnaireResponse,
    physicalexam_aidbox_QuestionnaireResponse,
    physicalexam_fhir_QuestionnaireResponse,
    reviewofsystems_aidbox_QuestionnaireResponse,
    reviewofsystems_fhir_QuestionnaireResponse,
    vitals_aidbox_QuestionnaireResponse,
    vitals_fhir_QuestionnaireResponse,
)


def load_json_file(file_path):
    with open(file_path, "r") as f:
        json_data = f.read()
    return json.loads(json_data)


def test_fhir_to_fce_QuestionnaireResponse():
    fhir_file_path = "tests/fce/resources/questionnaire_response_fhir/practitioner.json"
    fce_file_path = "tests/fce/resources/questionnaire_response_fce/practitioner.json"
    fhir_practitioner = load_json_file(fhir_file_path)
    fce_practitioner = load_json_file(fce_file_path)
    assert to_first_class_extension(fhir_practitioner) == fce_practitioner

    assert (
        to_first_class_extension(patient_fhir_QuestionnaireResponse)
        == patient_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(allergies_fhir_QuestionnaireResponse)
        == allergies_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(gad7_fhir_QuestionnaireResponse)
        == gad7_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(medication_fhir_QuestionnaireResponse)
        == medication_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(physicalexam_fhir_QuestionnaireResponse)
        == physicalexam_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(reviewofsystems_fhir_QuestionnaireResponse)
        == reviewofsystems_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(vitals_fhir_QuestionnaireResponse)
        == vitals_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(phq2phq9_fhir_QuestionnaireResponse)
        == phq2phq9_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(immunization_fhir_QuestionnaireResponse)
        == immunization_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(cardiology_fhir_QuestionnaireResponse)
        == cardiology_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(allergies_inprogress_fhir_QuestionnaireResponse)
        == allergies_inprogress_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(newappointment_fhir_QuestionnaireResponse)
        == newappointment_aidbox_QuestionnaireResponse
    )
    assert (
        to_first_class_extension(few_answers_fhir_questionnaire_response)
        == few_answers_aidbox_questionnaire_response
    )


@pytest.mark.parametrize(
    "filename",
    [
        "choice_answer_option.json",
        "beverages.json",
        "allergies.json",
        "encounter_create.json",
        "gad_7.json",
        "immunization.json",
        "medication.json",
        "patient_create.json",
        "patient_edit.json",
        "phq_2_phq_9.json",
        "physicalexam.json",
        "practitioner_create.json",
        "practitioner_edit.json",
        "practitioner_role_create.json",
        "public_appointment.json",
        "review_of_systems.json",
        "vitals.json",
        "source_queries.json",
        "multiple_type_launch_context.json",
        "practitioner_create_structure_map.json",
    ],
)
def test_fhir_to_fce_questionnaire(filename):
    fhir_data = load_json_file(f"tests/fce/resources/questionnaire_fhir/{filename}")
    fce_data = load_json_file(f"tests/fce/resources/questionnaire_fce/{filename}")
    assert to_first_class_extension(fhir_data) == fce_data
