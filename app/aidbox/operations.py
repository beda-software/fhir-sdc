import json

from aiohttp import web

from ..sdc import (
    assemble,
    constraint_check,
    extract_questionnaire,
    extract_questionnaire_instance,
    get_questionnaire_context,
    populate,
    resolve_expression,
)
from ..sdc.utils import parameter_to_env
from .sdk import sdk
from .utils import get_user_sdk_client


@sdk.operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
async def assemble_op(_operation, request):
    client = get_user_sdk_client(request)
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request["route-params"]["id"]).get()
    )

    assembled_questionnaire = await assemble(client, questionnaire)
    return web.json_response(assembled_questionnaire, dumps=lambda a: json.dumps(a, default=list))


@sdk.operation(["POST"], ["QuestionnaireResponse", "$constraint-check"])
async def constraint_check_operation(_operation, request):
    env = parameter_to_env(request["resource"])
    questionnaire = env["Questionnaire"]
    client = (
        request["app"]["client"]
        if questionnaire.get("runOnBehalfOfRoot")
        else get_user_sdk_client(request)
    )

    return web.json_response(await constraint_check(client, env))


@sdk.operation(["POST"], ["Questionnaire", "$context"])
async def get_questionnaire_context_operation(_operation, request):
    client = request["app"]["client"]
    env = parameter_to_env(request["resource"])
    questionnaire = env["Questionnaire"]
    client = (
        request["app"]["client"]
        if questionnaire.get("runOnBehalfOfRoot")
        else get_user_sdk_client(request)
    )

    return web.json_response(await get_questionnaire_context(client, env))


@sdk.operation(["POST"], ["Questionnaire", "$extract"])
async def extract_questionnaire_operation(_operation, request):
    resource = request["resource"]
    client = request["app"]["client"]
    jute_service = request["app"]["settings"].JUTE_SERVICE
    run_on_behalf_of_root = False
    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire = (
            await client.resources("Questionnaire").search(_id=resource["questionnaire"]).get()
        )
        run_on_behalf_of_root = questionnaire.get("runOnBehalfOfRoot")
    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request["resource"])
        questionnaire = env.get("Questionnaire")
        run_on_behalf_of_root = questionnaire.get("runOnBehalfOfRoot")
    client = request["app"]["client"] if run_on_behalf_of_root else get_user_sdk_client(request)

    return web.json_response(await extract_questionnaire(client, resource, jute_service))


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
async def extract_questionnaire_instance_operation(_operation, request):
    resource = request["resource"]
    client = request["app"]["client"]
    jute_service = request["app"]["settings"].JUTE_SERVICE
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request["route-params"]["id"]).get()
    )
    client = (
        request["app"]["client"]
        if questionnaire.get("runOnBehalfOfRoot")
        else get_user_sdk_client(request)
    )
    return web.json_response(
        await extract_questionnaire_instance(client, questionnaire, resource, jute_service)
    )


@sdk.operation(["POST"], ["Questionnaire", "$populate"])
async def populate_questionnaire(_operation, request):
    client = request["app"]["client"]
    env = parameter_to_env(request["resource"])

    questionnaire_data = env["Questionnaire"]
    if not questionnaire_data:
        # TODO: return OperationOutcome
        return web.json_response(
            {
                "error": "bad_request",
                "error_description": "`Questionnaire` parameter is required",
            },
            status=422,
        )

    questionnaire = client.resource("Questionnaire", **questionnaire_data)
    client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)

    populated_resource = await populate(client, questionnaire, env)
    return web.json_response(populated_resource)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
async def populate_questionnaire_instance(_operation, request):
    client = request["app"]["client"]
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request["route-params"]["id"]).get()
    )
    env = parameter_to_env(request["resource"])
    env["Questionnaire"] = questionnaire
    client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)

    populated_resource = await populate(client, questionnaire, env)
    return web.json_response(populated_resource)


@sdk.operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return web.json_response(resolve_expression(request["resource"]))
