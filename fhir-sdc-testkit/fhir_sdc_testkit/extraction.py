"""Raising for a failed `$extract`, whichever shape the server answers with.

fhir-sdc answers with a list of result bundles; SDC defines `Parameters` with `return` and `issues`;
a failure may also come back as a bare OperationOutcome.
"""

from collections.abc import Mapping, Sequence
from typing import Any

import fhirpy_types_r4b as r4b

# $extract echoes back what the mappers created, which may be resources R4B does not model.
Json = Mapping[str, Any]
ExtractionResult = Sequence[Json] | Json
FAILED_SEVERITIES = ("error", "fatal")
SUCCESSFUL_CODES = range(200, 300)


class ExtractionError(Exception):
    """A failure the server reported in a successful `$extract` response."""


def raise_for_extraction_errors(extracted: ExtractionResult) -> None:
    if not isinstance(extracted, Mapping):
        for bundle in extracted:
            raise_for_rejected_entries(bundle)
        return

    resource_type = extracted.get("resourceType")
    if resource_type == "OperationOutcome":
        raise ExtractionError(str(extracted))

    if resource_type != "Parameters":
        raise ExtractionError(f"Unexpected $extract response: {resource_type}")

    for parameter in extracted.get("parameter") or []:
        if parameter["name"] == "return":
            raise_for_rejected_entries(parameter["resource"])
        elif parameter["name"] == "issues":
            raise_for_failed_issues(parameter["resource"])


def raise_for_rejected_entries(bundle: Json) -> None:
    """A batch reports a rejected entry in the entry's response, under HTTP 200 for the bundle."""
    for entry in bundle.get("entry") or []:
        response = entry.get("response")
        if response is not None and not is_successful_status(response.get("status", "")):
            raise ExtractionError(f"{entry.get('request', {})} -> {response}")


def is_successful_status(status: str) -> bool:
    """An entry status leads with the HTTP code, as in `201 Created`."""
    code = status.split(maxsplit=1)[0] if status else ""
    return code.isdigit() and int(code) in SUCCESSFUL_CODES


def raise_for_failed_issues(outcome: Json) -> None:
    """SDC puts hints and warnings in `issues` on success, so only error and fatal are failures."""
    issues = r4b.OperationOutcome.model_validate(outcome).issue
    failures = [issue for issue in issues if issue.severity in FAILED_SEVERITIES]
    if failures:
        raise ExtractionError(str(failures))
