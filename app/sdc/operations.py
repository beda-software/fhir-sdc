from dataclasses import dataclass
from typing import Any

from fhirpy import AsyncFHIRClient

from .assemble import assemble
from .constraint_check import constraint_check
from .context import load_questionnaire_context
from .exception import MissingParamOperationOutcome
from .extract import build_extract_bundle
from .populate import populate
from .utils import is_sdc_api, parse_parameters, resolve_questionnaire, resolve_questionnaire_by_id


@dataclass
class SdcContext:
    user_client: AsyncFHIRClient
    extract_services: dict


async def run_assemble(ctx: SdcContext, questionnaire_id: str) -> dict:
    questionnaire = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    return await assemble(ctx.user_client, questionnaire)


async def run_populate(
    ctx: SdcContext, parameters: dict, questionnaire_id: str | None = None
) -> dict:
    questionnaire, _, variables = await parse_parameters(ctx.user_client, parameters)
    if questionnaire_id:
        questionnaire = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    return await populate(
        ctx.user_client,
        require_param(questionnaire, "Questionnaire"),
        variables,
        sdc_api=is_sdc_api(parameters),
    )


async def run_extract(ctx: SdcContext, resource: dict, questionnaire_id: str | None = None) -> list:
    # The Questionnaire the route names wins: a caller cannot swap it through the body.
    route_questionnaire = (
        await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
        if questionnaire_id
        else None
    )
    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = ctx.user_client.resource("QuestionnaireResponse", **resource)
        variables = {}
        questionnaire = route_questionnaire or await resolve_questionnaire(
            ctx.user_client, resource.get("questionnaire")
        )
    elif resource["resourceType"] == "Parameters":
        questionnaire, questionnaire_response, variables = await parse_parameters(
            ctx.user_client, resource
        )
        require_param(questionnaire_response, "QuestionnaireResponse")
        questionnaire = route_questionnaire or questionnaire
    else:
        raise MissingParamOperationOutcome(
            "Either `QuestionnaireResponse` resource or Parameters containing "
            "QuestionnaireResponse are required",
        )

    bundle = await build_checked_extract_bundle(
        ctx, require_param(questionnaire, "Questionnaire"), questionnaire_response, variables
    )
    return [await ctx.user_client.execute("/", data=bundle)] if bundle else []


async def run_questionnaire_response_extract(
    ctx: SdcContext, parameters: dict, questionnaire_response_id: str | None = None
) -> dict:
    """SDC `$extract`: return the bundle for the client to submit instead of submitting it."""
    questionnaire, questionnaire_response, variables = await parse_parameters(
        ctx.user_client, parameters
    )
    if questionnaire_response_id:
        questionnaire_response = dict(
            await ctx.user_client.resources("QuestionnaireResponse")
            .search(_id=questionnaire_response_id)
            .get()
        )
    require_param(questionnaire_response, "questionnaire-response")
    questionnaire = questionnaire or await resolve_questionnaire(
        ctx.user_client, questionnaire_response.get("questionnaire")
    )
    bundle = await build_checked_extract_bundle(
        ctx, questionnaire, questionnaire_response, variables
    )
    return build_extract_output(bundle)


async def build_checked_extract_bundle(
    ctx: SdcContext,
    questionnaire: dict,
    questionnaire_response: dict,
    variables: dict[str, Any],
) -> dict | None:
    await constraint_check(ctx.user_client, questionnaire, questionnaire_response, variables)
    return await build_extract_bundle(
        ctx.user_client, questionnaire, questionnaire_response, variables, ctx.extract_services
    )


def build_extract_output(bundle: dict | None) -> dict:
    """SDC `$extract` output: the bundle to submit in `return`, or why there is none in `issues`."""
    if bundle and bundle["entry"]:
        return {"resourceType": "Parameters", "parameter": [{"name": "return", "resource": bundle}]}

    nothing_extracted = {
        "resourceType": "OperationOutcome",
        "issue": [
            {
                "severity": "information",
                "code": "informational",
                "diagnostics": "Nothing to extract",
            }
        ],
    }
    return {
        "resourceType": "Parameters",
        "parameter": [{"name": "issues", "resource": nothing_extracted}],
    }


async def run_constraint_check(ctx: SdcContext, parameters: dict) -> dict:
    questionnaire, questionnaire_response, variables = await parse_parameters(
        ctx.user_client, parameters
    )
    return await constraint_check(
        ctx.user_client,
        require_param(questionnaire, "Questionnaire"),
        require_param(questionnaire_response, "QuestionnaireResponse"),
        variables,
    )


async def run_context(ctx: SdcContext, parameters: dict) -> dict:
    questionnaire, questionnaire_response, variables = await parse_parameters(
        ctx.user_client, parameters
    )
    return await load_questionnaire_context(
        ctx.user_client,
        require_param(questionnaire, "Questionnaire"),
        questionnaire_response,
        variables,
    )


def require_param(value: dict | None, name: str) -> dict:
    if not value:
        raise MissingParamOperationOutcome(f"`{name}` parameter is required")

    return value
