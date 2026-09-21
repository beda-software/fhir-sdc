from aiohttp import web
from fhirpy.base.exceptions import OperationOutcome

# The Aidbox SDK answers every raised outcome with 422, so both apps report failures alike.
OPERATION_OUTCOME_STATUS = 422


@web.middleware
async def render_operation_outcome(request: web.Request, handler):
    try:
        return await handler(request)
    except OperationOutcome as exc:
        return web.json_response(exc.resource, status=OPERATION_OUTCOME_STATUS)
