from app.converter.fhir_to_fce import to_first_class_extension
from tests.fce.resources.fce import (
    patient_fhir_QuestionnaireResponse,
    patient_aidbox_QuestionnaireResponse,
    practitioner_aidbox_QuestionnaireResponse,
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
    beverages_fhir_Questionnaire,
    beverages_aidbox_Questionnaire,
    allergies_fhir_Questionnaire,
    allergies_aidbox_Questionnaire,
    encounter_create_fhir_Questionnaire,
    encounter_create_aidbox_Questionnaire,
    gad7_fhir_Questionnaire,
    gad7_aidbox_Questionnaire,
    immunization_fhir_Questionnaire,
    immunization_aidbox_Questionnaire,
    medication_fhir_Questionnaire,
    medication_aidbox_Questionnaire,
    patient_create_fhir_Questionnaire,
    patient_create_aidbox_Questionnaire,
    patient_edit_fhir_Questionnaire,
    patient_edit_aidbox_Questionnaire,
    phq2phq9_fhir_Questionnaire,
    phq2phq9_aidbox_Questionnaire,
    physicalexam_fhir_Questionnaire,
    physicalexam_aidbox_Questionnaire,
    practitioner_create_fhir_Questionnaire,
    practitioner_create_aidbox_Questionnaire,
    practitioner_edit_fhir_Questionnaire,
    practitioner_edit_aidbox_Questionnaire,
    practitioner_role_create_fhir_Questionnaire,
    practitioner_role_create_aidbox_Questionnaire,
    public_appointment_fhir_Questionnaire,
    public_appointment_aidbox_Questionnaire,
    review_of_systems_fhir_Questionnaire,
    review_of_systems_aidbox_Questionnaire,
    vitals_fhir_Questionnaire,
    vitals_aidbox_Questionnaire,
    # practitioner_fhir_QuestionnaireResponse,
    source_queries_aidbox_questionnaire,
    source_queries_fhir_questionnaire,
    few_answers_fhir_questionnaire_response,
    few_answers_aidbox_questionnaire_response,
    multiple_type_fhir_Questionnaire,
    multiple_type_aidbox_Questionnaire,
)

import json


def load_json_file(file_path):
    with open(file_path, "r") as f:
        json_data = f.read()
    return json.loads(json_data)


def test_fhir_to_fce_QuestionnaireResponse():
    fhir_file_path = 'tests/fce/resources/fhir_questionnaire_response/practitioner.json'
    fhir_practitioner = load_json_file(fhir_file_path)
    assert to_first_class_extension(fhir_practitioner) == practitioner_aidbox_QuestionnaireResponse
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

def test_fhir_to_fce_Questionnaire():
    fhir_file_path = 'tests/fce/resources/fhir_questionnaire/choice_reference.json'
    fce_file_path = 'tests/fce/resources/fce_questionnaire/choice_reference.json'
    fhir_choice_refernce = load_json_file(fhir_file_path)
    fce_choice_refernce = load_json_file(fce_file_path)
    assert to_first_class_extension(fhir_choice_refernce) == fce_choice_refernce
    assert to_first_class_extension(beverages_fhir_Questionnaire) == beverages_aidbox_Questionnaire
    assert to_first_class_extension(allergies_fhir_Questionnaire) == allergies_aidbox_Questionnaire
    assert (
        to_first_class_extension(encounter_create_fhir_Questionnaire)
        == encounter_create_aidbox_Questionnaire
    )
    assert to_first_class_extension(gad7_fhir_Questionnaire) == gad7_aidbox_Questionnaire
    assert (
        to_first_class_extension(immunization_fhir_Questionnaire)
        == immunization_aidbox_Questionnaire
    )
    assert (
        to_first_class_extension(medication_fhir_Questionnaire) == medication_aidbox_Questionnaire
    )
    assert (
        to_first_class_extension(patient_create_fhir_Questionnaire)
        == patient_create_aidbox_Questionnaire
    )
    assert (
        to_first_class_extension(patient_edit_fhir_Questionnaire)
        == patient_edit_aidbox_Questionnaire
    )
    assert to_first_class_extension(phq2phq9_fhir_Questionnaire) == phq2phq9_aidbox_Questionnaire
    assert (
        to_first_class_extension(physicalexam_fhir_Questionnaire)
        == physicalexam_aidbox_Questionnaire
    )
    assert (
        to_first_class_extension(practitioner_create_fhir_Questionnaire)
        == practitioner_create_aidbox_Questionnaire
    )
    assert (
        to_first_class_extension(practitioner_edit_fhir_Questionnaire)
        == practitioner_edit_aidbox_Questionnaire
    )
    assert (
        to_first_class_extension(practitioner_role_create_fhir_Questionnaire)
        == practitioner_role_create_aidbox_Questionnaire
    )
    assert (
        to_first_class_extension(public_appointment_fhir_Questionnaire)
        == public_appointment_aidbox_Questionnaire
    )
    assert (
        to_first_class_extension(review_of_systems_fhir_Questionnaire)
        == review_of_systems_aidbox_Questionnaire
    )
    assert to_first_class_extension(vitals_fhir_Questionnaire) == vitals_aidbox_Questionnaire
    assert (
        to_first_class_extension(source_queries_fhir_questionnaire)
        == source_queries_aidbox_questionnaire
    )
    assert (
        to_first_class_extension(multiple_type_fhir_Questionnaire)
        == multiple_type_aidbox_Questionnaire
    )
