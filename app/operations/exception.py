from fhirpy.base.exceptions import OperationOutcome


class ConstraintCheckOperationOutcome(OperationOutcome):
    def __init__(self, validation_errors):
        OperationOutcome.__init__(
            self,
            resource={
                "resourceType": "OperationOutcome",
                "issue": [
                    # TODO: check how to proper map Constraint to OperationOutcome issue
                    {
                        "severity": e["severity"],
                        "code": e["key"],
                        "diagnostics": e["human"],
                    }
                    for e in validation_errors
                ],
            },
        )
