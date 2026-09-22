import json

from aiohttp import web

from app.sdc.exception import ConstraintCheckOperationOutcome, MissingParamOperationOutcome
from app.sdc.getters import QUESTIONNAIRE_MAPPER_URL, TARGET_STRUCTURE_MAP_URL

from ..sdc import (
    assemble,
    constraint_check,
    extract,
    get_questionnaire_context,
    populate,
    resolve_expression,
)
from ..sdc.utils import is_sdc_api, parameter_to_env, resolve_questionnaire
from ..utils import get_extract_services
from .utils import build_user_client

routes = web.RouteTableDef()


async def _build_mapper_templates(client, questionnaire: dict) -> list:
    mapper_templates = []
    for ext in questionnaire.get("extension", []):
        if ext["url"] == TARGET_STRUCTURE_MAP_URL:
            structure_map_id = ext["valueCanonical"].split("/")[-1]
            structure_map = (
                await client.resources("StructureMap").search(_id=structure_map_id).get()
            )
            template_string = structure_map.get_by_path(
                [
                    "group",
                    {"name": "jute-group"},
                    "rule",
                    {"name": "apply-jute"},
                    "extension",
                    {"url": "http://beda.software/fhir-extensions/jute-body"},
                    "valueString",
                ]
            )
            mapper_templates.append(json.loads(template_string))
        elif ext["url"] == QUESTIONNAIRE_MAPPER_URL:
            value_expression = ext.get("valueExpression")
            if value_expression and value_expression.get("expression"):
                mapper_templates.append(json.loads(value_expression["expression"]))
    return mapper_templates


@routes.get("/Questionnaire/{id}/$assemble")
async def assemble_handler(request: web.BaseRequest):
    client = build_user_client(request)

    questionnaire = (
        await client.resources("Questionnaire").search(_id=request.match_info["id"]).get()
    )

    assembled_questionnaire_lazy = await assemble(client, dict(questionnaire))
    assembled_questionnaire = json.loads(json.dumps(assembled_questionnaire_lazy, default=list))

    return web.json_response(assembled_questionnaire)


@routes.post("/QuestionnaireResponse/$constraint-check")
async def constraint_check_handler(request: web.BaseRequest):
    client = build_user_client(request)
    env = await parameter_to_env(client, await request.json())

    return web.json_response(
        await constraint_check(
            client,
            env["Questionnaire"],
            env,
        )
    )


@routes.post("/Questionnaire/$context")
async def get_questionnaire_context_handler(request: web.BaseRequest):
    client = build_user_client(request)
    env = await parameter_to_env(client, await request.json())

    return web.json_response(await get_questionnaire_context(client, env["Questionnaire"], env))


@routes.post("/Questionnaire/$extract")
async def extract_questionnaire_handler(request: web.BaseRequest):
    resource = await request.json()
    client = build_user_client(request)

    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        questionnaire_response = resource
        questionnaire = await resolve_questionnaire(client, resource.get("questionnaire"))
    elif resource["resourceType"] == "Parameters":
        env = await parameter_to_env(client, resource)
        questionnaire = env.get("Questionnaire")
        questionnaire_response = env.get("QuestionnaireResponse")

    mapper_templates = await _build_mapper_templates(client, questionnaire)

    context = {
        "Questionnaire": questionnaire,
        "QuestionnaireResponse": questionnaire_response,
        **env,
    }

    await constraint_check(
        client,
        questionnaire,
        context,
    )
    extraction_result = await extract(
        client, mapper_templates, context, get_extract_services(request.app)
    )
    return web.json_response(extraction_result)


@routes.post("/Questionnaire/{id}/$extract")
async def extract_questionnaire_instance_operation(request: web.BaseRequest):
    resource = await request.json()
    client = build_user_client(request)
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request.match_info["id"]).get()
    )

    mapper_templates = await _build_mapper_templates(client, questionnaire)

    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = client.resource("QuestionnaireResponse", **resource)
        context = {
            "Questionnaire": questionnaire,
            "QuestionnaireResponse": questionnaire_response,
        }
        await constraint_check(
            client,
            questionnaire,
            context,
        )
        return web.json_response(
            await extract(client, mapper_templates, context, get_extract_services(request.app))
        )

    if resource["resourceType"] == "Parameters":
        env = await parameter_to_env(client, resource)

        questionnaire_response_data = env.get("QuestionnaireResponse")
        if not questionnaire_response_data:
            raise ConstraintCheckOperationOutcome(
                [
                    {
                        "severity": "error",
                        "key": "missing-parameter",
                        "human": "`QuestionnaireResponse` parameter is required",
                    }
                ]
            )

        questionnaire_response = client.resource(
            "QuestionnaireResponse", **questionnaire_response_data
        )
        context = {
            "QuestionnaireResponse": questionnaire_response,
            "Questionnaire": questionnaire,
            **env,
        }
        await constraint_check(
            client,
            questionnaire,
            context,
        )
        return web.json_response(
            await extract(client, mapper_templates, context, get_extract_services(request.app))
        )

    raise ConstraintCheckOperationOutcome(
        [
            {
                "severity": "error",
                "key": "missing-parameter",
                "human": "Either `QuestionnaireResponse` resource or Parameters containing "
                "QuestionnaireResponse are required",
            }
        ]
    )


@routes.post("/Questionnaire/$populate")
async def populate_questionnaire_handler(request: web.BaseRequest):
    client = build_user_client(request)
    body = await request.json()
    env = await parameter_to_env(client, body)
    questionnaire_data = env.get("Questionnaire")
    if not questionnaire_data:
        raise MissingParamOperationOutcome("`Questionnaire` parameter is required")

    populated_resource = await populate(client, questionnaire_data, env, sdc_api=is_sdc_api(body))
    return web.json_response(populated_resource)


@routes.post("/Questionnaire/{id}/$populate")
async def populate_questionnaire_instance(request: web.BaseRequest):
    client = build_user_client(request)
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request.match_info["id"]).get()
    )
    body = await request.json()
    env = await parameter_to_env(client, body)
    env["Questionnaire"] = questionnaire
    populated_resource = await populate(client, questionnaire, env, sdc_api=is_sdc_api(body))

    return web.json_response(populated_resource)


@routes.post("/Questionnaire/$resolve-expression")
async def resolve_expression_operation_handler(request: web.BaseRequest):
    return web.json_response(resolve_expression(await request.json()))


@routes.get("/healthcheck")
async def healthcheck(request: web.BaseRequest):
    return web.json_response({"status": "ok"})
