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
from .utils import (
    is_sdc_api,
    parameter_to_env,
    rebuild_at_external_fhir_base_url,
    resolve_questionnaire,
    resolve_questionnaire_by_id,
)


@dataclass
class SdcContext:
    # The caller, at our FHIR server; rebuild_at_external_fhir_base_url moves it to the caller's data server.
    user_client: AsyncFHIRClient
    extract_services: dict


async def run_assemble(ctx: SdcContext, questionnaire_id: str) -> dict:
    questionnaire = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    assembled = await assemble(ctx.user_client, dict(questionnaire))
    return json.loads(json.dumps(assembled, default=list))


async def run_populate(ctx: SdcContext, parameters: dict, questionnaire_id: str | None = None):
    client = rebuild_at_external_fhir_base_url(ctx.user_client, parameters)
    env = await parameter_to_env(client, parameters)
    if questionnaire_id:
        env["Questionnaire"] = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    questionnaire = require_questionnaire(env.get("Questionnaire"))
    return await populate(client, questionnaire, env, sdc_api=is_sdc_api(parameters))


async def run_extract(ctx: SdcContext, resource: dict, questionnaire_id: str | None = None):
    client = rebuild_at_external_fhir_base_url(ctx.user_client, resource)
    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        questionnaire_response = client.resource("QuestionnaireResponse", **resource)
    elif resource["resourceType"] == "Parameters":
        env = await parameter_to_env(client, resource)
        if "QuestionnaireResponse" not in env:
            raise MissingParamOperationOutcome("`QuestionnaireResponse` parameter is required")

        questionnaire_response = env["QuestionnaireResponse"]
    else:
        raise MissingParamOperationOutcome(
            "Either `QuestionnaireResponse` resource or Parameters containing "
            "QuestionnaireResponse are required",
        )

    if questionnaire_id:
        questionnaire = dict(await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id))
    elif resource["resourceType"] == "QuestionnaireResponse":
        canonical = resource.get("questionnaire")
        questionnaire = dict(await resolve_questionnaire(ctx.user_client, canonical))
    else:
        questionnaire = env.get("Questionnaire")
    questionnaire = require_questionnaire(questionnaire)

    context = {
        "QuestionnaireResponse": questionnaire_response,
        "Questionnaire": questionnaire,
        **env,
    }
    mappers = await load_mappers(ctx.user_client, questionnaire)
    await constraint_check(client, questionnaire, context)
    return await extract(client, mappers, context, ctx.extract_services)


async def run_constraint_check(ctx: SdcContext, parameters: dict):
    client = rebuild_at_external_fhir_base_url(ctx.user_client, parameters)
    env = await parameter_to_env(client, parameters)
    return await constraint_check(client, require_questionnaire(env.get("Questionnaire")), env)


async def run_context(ctx: SdcContext, parameters: dict):
    client = rebuild_at_external_fhir_base_url(ctx.user_client, parameters)
    env = await parameter_to_env(client, parameters)
    return await get_questionnaire_context(
        client, require_questionnaire(env.get("Questionnaire")), env
    )


def require_questionnaire(questionnaire):
    if not questionnaire:
        raise MissingParamOperationOutcome("`Questionnaire` parameter is required")

    return questionnaire
