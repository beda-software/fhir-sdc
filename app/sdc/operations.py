from dataclasses import dataclass

from fhirpy import AsyncFHIRClient

from .assemble import assemble
from .constraint_check import constraint_check
from .context import get_questionnaire_context
from .exception import MissingParamOperationOutcome
from .extract import build_extract_bundle
from .mappers import load_mappers
from .populate import populate
from .utils import (
    build_legacy_extract_input,
    find_parameter_resource,
    is_sdc_api,
    parameter_to_env,
    resolve_questionnaire,
    resolve_questionnaire_by_id,
)


@dataclass
class SdcContext:
    user_client: AsyncFHIRClient
    extract_services: dict


async def run_assemble(ctx: SdcContext, questionnaire_id: str) -> dict:
    questionnaire = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    return await assemble(ctx.user_client, dict(questionnaire))


async def run_populate(ctx: SdcContext, parameters: dict, questionnaire_id: str | None = None):
    env = await parameter_to_env(ctx.user_client, parameters)
    if questionnaire_id:
        env["Questionnaire"] = await resolve_questionnaire_by_id(ctx.user_client, questionnaire_id)
    questionnaire = env.get("Questionnaire")
    require_questionnaire(questionnaire)
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

    require_questionnaire(questionnaire)
    # The Questionnaire the route names wins: a caller cannot swap it through the Parameters.
    context = {
        **env,
        "QuestionnaireResponse": questionnaire_response,
        "Questionnaire": questionnaire,
    }
    bundle = await build_questionnaire_extract_bundle(ctx, questionnaire, context)
    return [await ctx.user_client.execute("/", data=bundle)] if bundle else []


async def run_questionnaire_response_extract(
    ctx: SdcContext, parameters: dict, questionnaire_response_id: str | None = None
) -> dict:
    """SDC `$extract`: return the bundle for the client to submit instead of submitting it."""
    if questionnaire_response_id:
        questionnaire_response = dict(
            await ctx.user_client.resources("QuestionnaireResponse")
            .search(_id=questionnaire_response_id)
            .get()
        )
    else:
        questionnaire_response = find_parameter_resource(parameters, "questionnaire-response")
    if questionnaire_response is None:
        raise MissingParamOperationOutcome("`questionnaire-response` parameter is required")

    env = await parameter_to_env(
        ctx.user_client, build_legacy_extract_input(parameters, questionnaire_response)
    )
    questionnaire = env.get("Questionnaire") or dict(
        await resolve_questionnaire(ctx.user_client, questionnaire_response.get("questionnaire"))
    )
    context = {**env, "Questionnaire": questionnaire}
    bundle = await build_questionnaire_extract_bundle(ctx, questionnaire, context)
    return build_extract_output(bundle)


async def run_constraint_check(ctx: SdcContext, parameters: dict):
    env = await parameter_to_env(ctx.user_client, parameters)
    questionnaire = env.get("Questionnaire")
    require_questionnaire(questionnaire)
    if "QuestionnaireResponse" not in env:
        raise MissingParamOperationOutcome("`QuestionnaireResponse` parameter is required")

    return await constraint_check(ctx.user_client, questionnaire, env)


async def run_context(ctx: SdcContext, parameters: dict):
    env = await parameter_to_env(ctx.user_client, parameters)
    questionnaire = env.get("Questionnaire")
    require_questionnaire(questionnaire)
    return await get_questionnaire_context(ctx.user_client, questionnaire, env)


async def build_questionnaire_extract_bundle(
    ctx: SdcContext, questionnaire: dict, context: dict
) -> dict | None:
    mappers = await load_mappers(ctx.user_client, questionnaire)
    await constraint_check(ctx.user_client, questionnaire, context)
    return await build_extract_bundle(mappers, context, ctx.extract_services)


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


def require_questionnaire(questionnaire: dict | None) -> None:
    if not questionnaire:
        raise MissingParamOperationOutcome("`Questionnaire` parameter is required")
