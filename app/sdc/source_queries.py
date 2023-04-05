from fhirpy.base.exceptions import OperationOutcome

from .utils import resolve_string_template


def resolve_expression(resource):
    try:
        env = resource["env"]
        expression = resource["expression"]
    except KeyError as e:
        raise OperationOutcome(str(e))

    resolved_expression = resolve_string_template(expression, env)
    return resolved_expression
