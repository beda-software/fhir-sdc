from fhirpy.base.exceptions import OperationOutcome

from .utils import resolve_string_template


def resolve_expression(resource):
    try:
        env = resource["env"]
        expression = resource["expression"]
    except KeyError as e:
        raise OperationOutcome(str(e)) from e

    return resolve_string_template({}, expression, env)
