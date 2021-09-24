from aiohttp import web

from app.sdk import sdk
from .utils import OperationOutcome, resolve_string_template


@sdk.operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
def resolve_expression(operation, request):
    try:
        env = request['resource']["env"]
        expression = request['resource']["expression"]
    except Exception as e:
        raise OperationOutcome(reason=str(e), status_code=422)

    resolved_expression = resolve_string_template(expression, env)
    return web.json_response(resolved_expression)
