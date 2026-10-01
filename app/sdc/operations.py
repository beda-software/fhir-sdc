from dataclasses import dataclass

import simplejson as json
from fhirpy import AsyncFHIRClient

from .assemble import assemble
from .constraint_check import constraint_check
from .context import get_questionnaire_context
from .exception import MissingParamOperationOutcome
from .extract import extract
from .mappers import load_mappers
from .populate import populate
from .utils import is_sdc_api, parameter_to_env, resolve_questionnaire, resolve_questionnaire_by_id


@dataclass
class SdcContext:
    user_client: AsyncFHIRClient
    extract_services: dict


async def run_assemble(ctx: SdcContext, questionnaire_id: str) -> dict:
    questionnaire = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    assembled = await assemble(ctx.user_client, dict(questionnaire))
    return json.loads(json.dumps(assembled, default=list))


async def run_populate(ctx: SdcContext, parameters: dict, questionnaire_id: str | None = None):
    named = (
        await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
        if questionnaire_id
        else None
    )
    env = await parameter_to_env(ctx.user_client, parameters)
    if named is not None:
        env["Questionnaire"] = named
    questionnaire = require_questionnaire(env.get("Questionnaire"))
    return await populate(ctx.user_client, questionnaire, env, sdc_api=is_sdc_api(parameters))


async def run_extract(ctx: SdcContext, resource: dict, questionnaire_id: str | None = None):
    questionnaire = (
        dict(await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id))
        if questionnaire_id
        else None
    )
    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        questionnaire_response = ctx.user_client.resource("QuestionnaireResponse", **resource)
        if questionnaire is None:
            canonical = resource.get("questionnaire")
            questionnaire = dict(await resolve_questionnaire(ctx.user_client, canonical))
    elif resource["resourceType"] == "Parameters":
        env = await parameter_to_env(ctx.user_client, resource)
        if "QuestionnaireResponse" not in env:
            raise MissingParamOperationOutcome("`QuestionnaireResponse` parameter is required")

        questionnaire_response = env["QuestionnaireResponse"]
        questionnaire = questionnaire or env.get("Questionnaire")
    else:
        raise MissingParamOperationOutcome(
            "Either `QuestionnaireResponse` resource or Parameters containing "
            "QuestionnaireResponse are required",
        )

    questionnaire = require_questionnaire(questionnaire)
    # The Questionnaire the route names wins: a caller cannot swap it through the Parameters.
    env["Questionnaire"] = questionnaire

    context = {
        "QuestionnaireResponse": questionnaire_response,
        "Questionnaire": questionnaire,
        **env,
    }
    mappers = await load_mappers(ctx.user_client, questionnaire)
    await constraint_check(ctx.user_client, questionnaire, context)
    return await extract(ctx.user_client, mappers, context, ctx.extract_services)


async def run_constraint_check(ctx: SdcContext, parameters: dict):
    env = await parameter_to_env(ctx.user_client, parameters)
    questionnaire = require_questionnaire(env.get("Questionnaire"))
    if "QuestionnaireResponse" not in env:
        raise MissingParamOperationOutcome("`QuestionnaireResponse` parameter is required")

    return await constraint_check(ctx.user_client, questionnaire, env)


async def run_context(ctx: SdcContext, parameters: dict):
    env = await parameter_to_env(ctx.user_client, parameters)
    return await get_questionnaire_context(
        ctx.user_client, require_questionnaire(env.get("Questionnaire")), env
    )


def require_questionnaire(questionnaire):
    if not questionnaire:
        raise MissingParamOperationOutcome("`Questionnaire` parameter is required")

    return questionnaire
