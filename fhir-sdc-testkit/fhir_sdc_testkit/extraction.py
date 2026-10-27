"""Raising for a failed SDC `QuestionnaireResponse/$extract` and for a rejected submission."""

from collections.abc import Mapping
from typing import Any

import fhirpy_types_r4b as r4b

# $extract returns what the mappers created, which may be resources R4B does not model.
Json = Mapping[str, Any]
FAILED_SEVERITIES = ("error", "fatal")
SUCCESSFUL_CODES = range(200, 300)


class ExtractionError(Exception):
    """A failure the server reported in a successful response."""


def raise_for_failed_issues(extracted: Json) -> None:
    """SDC puts hints and warnings in `issues` on success, so only error and fatal are failures."""
    for parameter in extracted.get("parameter") or []:
        if parameter["name"] == "issues":
            issues = r4b.OperationOutcome.model_validate(parameter["resource"]).issue
            failures = [issue for issue in issues if issue.severity in FAILED_SEVERITIES]
            if failures:
                raise ExtractionError(str(failures))


def find_bundle_to_submit(extracted: Json) -> dict[str, Any] | None:
    return next(
        (
            parameter["resource"]
            for parameter in extracted.get("parameter") or []
            if parameter["name"] == "return"
        ),
        None,
    )


def raise_for_rejected_entries(bundle: Json) -> None:
    """A batch reports a rejected entry in the entry's response, under HTTP 200 for the bundle."""
    for entry in bundle.get("entry") or []:
        if not is_successful_status(entry["response"]["status"]):
            raise ExtractionError(f"{entry.get('request', {})} -> {entry['response']}")


def is_successful_status(status: str) -> bool:
    """An entry status leads with the HTTP code, as in `201 Created`."""
    return int(status.split(maxsplit=1)[0]) in SUCCESSFUL_CODES
