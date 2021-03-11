import json

from aiohttp import web


class ConstraintCheckOperationOutcome(web.HTTPError):
    # TODO: use from aidbox-python-sdk
    status_code = 422

    def __init__(self, validation_errors):
        web.HTTPError.__init__(
            self,
            text=json.dumps(
                {
                    "resourceType": "OperationOutcome",
                    # "status": 400,
                    "issue": [
                        # TODO: check how to proper map Constraint to OperationOutcome issue
                        {
                            "severity": e["severity"],
                            "code": e["key"],
                            "diagnostics": e["human"],
                        }
                        for e in validation_errors
                    ],
                }
            ),
            content_type="application/json",
        )
