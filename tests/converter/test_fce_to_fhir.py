import pytest

from app.converter.fce_to_fhir import from_first_class_extension
from app.converter.utils import load_json_file


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
        "consent.json",
        "enable_when.json"
    ],
)
def test_fce_to_fhir_questionnaire(filename):
    fce_data = load_json_file(f"tests/converter/resources/questionnaire_fce/{filename}")
    fhir_data = load_json_file(f"tests/converter/resources/questionnaire_fhir/{filename}")
    assert from_first_class_extension(fce_data) == fhir_data


@pytest.mark.parametrize(
    "filename",
    [
        "allergies_inprogress.json",
        "cardiology.json",
        "few_answers.json",
        "gad_7.json",
        "immunization.json",
        "medication.json",
        "new_appointment.json",
        "patient.json",
        "phq_2_phq_9.json",
        "physicalexam.json",
        "practitioner.json",
        "review_of_systems.json",
        "vitals.json",
        "reference_answer_with_assoc.json",
    ],
)
def test_fce_to_fhir_questionnaireResponse(filename):
    fce_data = load_json_file(f"tests/converter/resources/questionnaire_response_fce/{filename}")
    fhir_data = load_json_file(f"tests/converter/resources/questionnaire_response_fhir/{filename}")
    assert from_first_class_extension(fce_data) == fhir_data
