import pytest

from fhir_sdc_testkit import ExtractionError
from fhir_sdc_testkit.extraction import (
    find_bundle_to_submit,
    raise_for_failed_issues,
    raise_for_rejected_entries,
)

REJECTED = {"response": {"status": "422", "outcome": {"issue": []}}}


def test_error_issue_raises() -> None:
    with pytest.raises(ExtractionError, match="error"):
        raise_for_failed_issues(build_issues("warning", "error"))


def test_warning_issues_pass() -> None:
    raise_for_failed_issues(build_issues("warning", "information"))


def test_return_bundle_is_found() -> None:
    bundle = {"resourceType": "Bundle", "type": "transaction", "entry": []}

    found = find_bundle_to_submit(
        {"resourceType": "Parameters", "parameter": [{"name": "return", "resource": bundle}]}
    )
    assert found == bundle


def test_missing_return_bundle_is_none() -> None:
    assert find_bundle_to_submit(build_issues("information")) is None


def test_rejected_entry_raises() -> None:
    with pytest.raises(ExtractionError, match="422"):
        raise_for_rejected_entries({"entry": [REJECTED]})


def test_accepted_entries_pass() -> None:
    raise_for_rejected_entries(
        {"entry": [{"response": {"status": "201 Created"}}, {"response": {"status": "200"}}]}
    )


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
