from app.converter.fce_to_fhir import from_first_class_extension
from tests.fce.resources.fce import (
    patient_fhir_QuestionnaireResponse,
    patient_aidbox_QuestionnaireResponse,
    allergies_fhir_QuestionnaireResponse,
    allergies_aidbox_QuestionnaireResponse,
    gad7_fhir_QuestionnaireResponse,
    gad7_aidbox_QuestionnaireResponse,
    medication_fhir_QuestionnaireResponse,
    medication_aidbox_QuestionnaireResponse,
    physicalexam_fhir_QuestionnaireResponse,
    physicalexam_aidbox_QuestionnaireResponse,
    reviewofsystems_fhir_QuestionnaireResponse,
    reviewofsystems_aidbox_QuestionnaireResponse,
    vitals_fhir_QuestionnaireResponse,
    vitals_aidbox_QuestionnaireResponse,
    phq2phq9_fhir_QuestionnaireResponse,
    phq2phq9_aidbox_QuestionnaireResponse,
    immunization_fhir_QuestionnaireResponse,
    immunization_aidbox_QuestionnaireResponse,
    cardiology_fhir_QuestionnaireResponse,
    cardiology_aidbox_QuestionnaireResponse,
    allergies_inprogress_fhir_QuestionnaireResponse,
    allergies_inprogress_aidbox_QuestionnaireResponse,
    newappointment_fhir_QuestionnaireResponse,
    newappointment_aidbox_QuestionnaireResponse,
    few_answers_fhir_questionnaire_response,
    few_answers_aidbox_questionnaire_response,
)

import json


def load_json_file(file_path):
    with open(file_path, "r") as f:
        json_data = f.read()
    return json.loads(json_data)


def test_fce_to_fhir_QuestionnaireResponse():
    fhir_file_path = "tests/fce/resources/questionnaire_response_fhir/practitioner.json"
    fce_file_path = "tests/fce/resources/questionnaire_response_fce/practitioner.json"
    fhir_practitioner = load_json_file(fhir_file_path)
    fce_practitioner = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_practitioner) == fhir_practitioner

    assert (
        from_first_class_extension(patient_aidbox_QuestionnaireResponse)
        == patient_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(allergies_aidbox_QuestionnaireResponse)
        == allergies_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(gad7_aidbox_QuestionnaireResponse)
        == gad7_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(medication_aidbox_QuestionnaireResponse)
        == medication_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(physicalexam_aidbox_QuestionnaireResponse)
        == physicalexam_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(reviewofsystems_aidbox_QuestionnaireResponse)
        == reviewofsystems_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(vitals_aidbox_QuestionnaireResponse)
        == vitals_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(phq2phq9_aidbox_QuestionnaireResponse)
        == phq2phq9_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(immunization_aidbox_QuestionnaireResponse)
        == immunization_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(cardiology_aidbox_QuestionnaireResponse)
        == cardiology_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(allergies_inprogress_aidbox_QuestionnaireResponse)
        == allergies_inprogress_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(newappointment_aidbox_QuestionnaireResponse)
        == newappointment_fhir_QuestionnaireResponse
    )
    assert (
        from_first_class_extension(few_answers_aidbox_questionnaire_response)
        == few_answers_fhir_questionnaire_response
    )


def test_fce_to_fhir_Questionnaire():
    fhir_file_path = "tests/fce/resources/questionnaire_fhir/choice_answer_option.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/choice_answer_option.json"
    fhir_choice_answer_option = load_json_file(fhir_file_path)
    fce_choice_answer_option = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_choice_answer_option) == fhir_choice_answer_option

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/beverages.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/beverages.json"
    fhir_beverages = load_json_file(fhir_file_path)
    fce_beverages = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_beverages) == fhir_beverages

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/allergies.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/allergies.json"
    fhir_allergies = load_json_file(fhir_file_path)
    fce_allergies = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_allergies) == fhir_allergies

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/encounter_create.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/encounter_create.json"
    fhir_encounter_create = load_json_file(fhir_file_path)
    fce_encounter_create = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_encounter_create) == fhir_encounter_create

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/gad_7.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/gad_7.json"
    fhir_gad_7 = load_json_file(fhir_file_path)
    fce_gad_7 = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_gad_7) == fhir_gad_7

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/immunization.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/immunization.json"
    fhir_immunization = load_json_file(fhir_file_path)
    fce_immunization = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_immunization) == fhir_immunization

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/medication.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/medication.json"
    fhir_medication = load_json_file(fhir_file_path)
    fce_medication = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_medication) == fhir_medication

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/patient_create.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/patient_create.json"
    fhir_patient_create = load_json_file(fhir_file_path)
    fce_patient_create = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_patient_create) == fhir_patient_create

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/patient_edit.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/patient_edit.json"
    fhir_patient_edit = load_json_file(fhir_file_path)
    fce_patient_edit = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_patient_edit) == fhir_patient_edit

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/phq_2_phq_9.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/phq_2_phq_9.json"
    fhir_phq_2_phq_9 = load_json_file(fhir_file_path)
    fce_phq_2_phq_9 = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_phq_2_phq_9) == fhir_phq_2_phq_9

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/physicalexam.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/physicalexam.json"
    fhir_physicalexam = load_json_file(fhir_file_path)
    fce_physicalexam = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_physicalexam) == fhir_physicalexam

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/practitioner_create.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/practitioner_create.json"
    fhir_practitioner_create = load_json_file(fhir_file_path)
    fce_practitioner_create = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_practitioner_create) == fhir_practitioner_create

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/practitioner_edit.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/practitioner_edit.json"
    fhir_practitioner_edit = load_json_file(fhir_file_path)
    fce_practitioner_edit = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_practitioner_edit) == fhir_practitioner_edit

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/practitioner_role_create.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/practitioner_role_create.json"
    fhir_practitioner_role_create = load_json_file(fhir_file_path)
    fce_practitioner_role_create = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_practitioner_role_create) == fhir_practitioner_role_create

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/public_appointment.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/public_appointment.json"
    fhir_public_appointment = load_json_file(fhir_file_path)
    fce_public_appointment = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_public_appointment) == fhir_public_appointment

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/review_of_systems.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/review_of_systems.json"
    fhir_review_of_systems = load_json_file(fhir_file_path)
    fce_review_of_systems = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_review_of_systems) == fhir_review_of_systems

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/vitals.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/vitals.json"
    fhir_vitals = load_json_file(fhir_file_path)
    fce_vitals = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_vitals) == fhir_vitals

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/source_queries.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/source_queries.json"
    fhir_source_queries = load_json_file(fhir_file_path)
    fce_source_queries = load_json_file(fce_file_path)
    assert from_first_class_extension(fce_source_queries) == fhir_source_queries

    fhir_file_path = "tests/fce/resources/questionnaire_fhir/multiple_type_launch_context.json"
    fce_file_path = "tests/fce/resources/questionnaire_fce/multiple_type_launch_context.json"
    fhir_multiple_type_launch_context = load_json_file(fhir_file_path)
    fce_multiple_type_launch_context = load_json_file(fce_file_path)
    assert (
        from_first_class_extension(fce_multiple_type_launch_context)
        == fhir_multiple_type_launch_context
    )
