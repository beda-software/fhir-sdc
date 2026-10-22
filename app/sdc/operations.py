from dataclasses import dataclass

from fhirpy import AsyncFHIRClient

from .assemble import assemble
from .constraint_check import constraint_check
from .context import get_questionnaire_context
from .exception import MissingParamOperationOutcome
from .extract import extract
from .mappers import load_mappers
from .populate import populate
from .utils import (
    build_fhirpath_env,
    is_sdc_api,
    parse_parameters,
    resolve_questionnaire,
    resolve_questionnaire_by_id,
)


@dataclass
class SdcContext:
    user_client: AsyncFHIRClient
    extract_services: dict


async def run_assemble(ctx: SdcContext, questionnaire_id: str) -> dict:
    questionnaire = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    return await assemble(ctx.user_client, questionnaire)


async def run_populate(ctx: SdcContext, parameters: dict, questionnaire_id: str | None = None):
    questionnaire, questionnaire_response, variables = await parse_parameters(
        ctx.user_client, parameters
    )
    if questionnaire_id:
        questionnaire = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    return await populate(
        ctx.user_client,
        require_param(questionnaire, "Questionnaire"),
        questionnaire_response,
        variables,
        sdc_api=is_sdc_api(parameters),
    )


async def run_extract(ctx: SdcContext, resource: dict, questionnaire_id: str | None = None):
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
        # The Questionnaire the route names wins: a caller cannot swap it through the Parameters.
        questionnaire = route_questionnaire or questionnaire
    else:
        raise MissingParamOperationOutcome(
            "Either `QuestionnaireResponse` resource or Parameters containing "
            "QuestionnaireResponse are required",
        )

    require_param(questionnaire, "Questionnaire")
    mappers = await load_mappers(ctx.user_client, questionnaire)
    await constraint_check(ctx.user_client, questionnaire, questionnaire_response, variables)
    env = build_fhirpath_env(questionnaire, questionnaire_response, variables)
    return await extract(ctx.user_client, mappers, env, ctx.extract_services)


async def run_constraint_check(ctx: SdcContext, parameters: dict):
    questionnaire, questionnaire_response, variables = await parse_parameters(
        ctx.user_client, parameters
    )
    return await constraint_check(
        ctx.user_client,
        require_param(questionnaire, "Questionnaire"),
        require_param(questionnaire_response, "QuestionnaireResponse"),
        variables,
    )


async def run_context(ctx: SdcContext, parameters: dict):
    questionnaire, questionnaire_response, variables = await parse_parameters(
        ctx.user_client, parameters
    )
    return await get_questionnaire_context(
        ctx.user_client,
        require_param(questionnaire, "Questionnaire"),
        questionnaire_response,
        variables,
    )


def require_param(value: dict | None, name: str) -> dict:
    if not value:
        raise MissingParamOperationOutcome(f"`{name}` parameter is required")

    return value
