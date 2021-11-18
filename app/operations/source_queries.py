from aiohttp import web
from fhirpy.base.exceptions import OperationOutcome

from app.sdk import sdk
from .utils import resolve_string_template


@sdk.operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
def resolve_expression(operation, request):
    try:
        env = request["resource"]["env"]
        expression = request["resource"]["expression"]
    except KeyError as e:
        raise OperationOutcome(str(e))

    resolved_expression = resolve_string_template(expression, env)
    return web.json_response(resolved_expression)
