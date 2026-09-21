import pytest
from fhirpy.base.exceptions import OperationOutcome, ResourceNotFound

from app.fhir_server.middlewares import render_operation_outcome
from app.sdc.exception import MissingParamOperationOutcome


def raising(error):
    async def handler(_request):
        raise error

    return handler


@pytest.mark.parametrize(
    "outcome",
    [
        MissingParamOperationOutcome("`Questionnaire` parameter is required"),
        OperationOutcome("the FHIR server rejected the bundle"),
    ],
)
async def test_an_outcome_is_answered_with_its_own_body(outcome):
    response = await render_operation_outcome(None, raising(outcome))
    assert response.status == 422
    assert outcome.resource["issue"][0]["diagnostics"] in response.text


async def test_an_upstream_failure_is_answered_with_a_bad_gateway():
    response = await render_operation_outcome(None, raising(ResourceNotFound("no resources found")))
    assert response.status == 502
    assert "no resources found" not in response.text
