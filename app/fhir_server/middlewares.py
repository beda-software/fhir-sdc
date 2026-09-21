import logging

from aiohttp import web
from aiohttp.typedefs import Handler
from fhirpy.base.exceptions import BaseFHIRError, IssueSeverity, IssueType, OperationOutcome

logger = logging.getLogger(__name__)

# The Aidbox SDK answers every outcome with 422, so both apps report a refusal alike.
REFUSED_STATUS = 422
UPSTREAM_FAILURE_STATUS = 502


@web.middleware
async def render_operation_outcome(request: web.Request, handler: Handler) -> web.StreamResponse:
    try:
        return await handler(request)
    except OperationOutcome as exc:
        return web.json_response(exc.resource, status=REFUSED_STATUS)
    except BaseFHIRError:
        logger.exception("The FHIR server answered with an error")
        outcome = OperationOutcome(
            "The FHIR server failed",
            severity=IssueSeverity.error.value,
            code=IssueType.exception.value,
        )
        return web.json_response(outcome.resource, status=UPSTREAM_FAILURE_STATUS)
