import fhirpy_types_r4b as r4b
import pytest

from fhir_sdc_testkit import launch_context
from fhir_sdc_testkit.sugar import build_context_parameter

PATIENT = r4b.Patient(id="patient-1")
PRACTITIONER = r4b.Practitioner(id="practitioner-1")


def test_context_parameter_carries_a_resource() -> None:
    parameter = build_context_parameter("Patient", [PATIENT])
    assert parameter.model_dump(exclude_none=True) == {
        "name": "context",
        "part": [
            {"name": "name", "valueString": "Patient"},
            {"name": "content", "resource": {"resourceType": "Patient", "id": "patient-1"}},
        ],
    }


def test_context_parameter_carries_a_reference() -> None:
    reference = r4b.Reference(reference="Patient/patient-1")

    parameter = build_context_parameter("Patient", [reference])
    assert parameter.model_dump(exclude_none=True) == {
        "name": "context",
        "part": [
            {"name": "name", "valueString": "Patient"},
            {"name": "content", "valueReference": {"reference": "Patient/patient-1"}},
        ],
    }


def test_context_parameter_carries_one_content_per_value() -> None:
    parameter = build_context_parameter("Authors", [PATIENT, PRACTITIONER])
    assert parameter.model_dump(exclude_none=True) == {
        "name": "context",
        "part": [
            {"name": "name", "valueString": "Authors"},
            {"name": "content", "resource": {"resourceType": "Patient", "id": "patient-1"}},
            {
                "name": "content",
                "resource": {"resourceType": "Practitioner", "id": "practitioner-1"},
            },
        ],
    }


def test_context_parameter_without_values_raises() -> None:
    with pytest.raises(ValueError, match="'Patient'"):
        build_context_parameter("Patient", [])


def test_launch_context_adds_the_subject() -> None:
    subject = r4b.Reference(reference="Patient/patient-1")

    parameters = launch_context({}, subject=subject)
    assert parameters.parameter == [r4b.ParametersParameter(name="subject", valueReference=subject)]


def test_launch_context_builds_one_parameter_per_name() -> None:
    parameters = launch_context({"Patient": PATIENT, "Authors": [PATIENT, PRACTITIONER]})
    assert parameters.parameter == [
        build_context_parameter("Patient", [PATIENT]),
        build_context_parameter("Authors", [PATIENT, PRACTITIONER]),
    ]
