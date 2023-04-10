import json

from aiohttp import web

from ..sdc import (
    assemble,
    constraint_check,
    extract,
    extract_questionnaire_instance,
    get_questionnaire_context,
    populate,
    resolve_expression,
)
from ..sdc.utils import parameter_to_env
from .sdk import sdk
from .utils import get_aidbox_fhir_client, get_user_sdk_client


@sdk.operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
@sdk.operation(["GET"], ["fhir", "Questionnaire", {"name": "id"}, "$assemble"])
async def assemble_op(operation, request):
    is_fhir = operation["request"][1] == "fhir"

    client = get_user_sdk_client(request)
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request["route-params"]["id"]).get()
    )

    assembled_questionnaire_lazy = await assemble(client, questionnaire)
    assembled_questionnaire = json.loads(json.dumps(assembled_questionnaire_lazy, default=list))
    if is_fhir:
        assembled_questionnaire = (
            await client.execute("$to-format/fhir", data=assembled_questionnaire)
        )["resource"]
    return web.json_response(assembled_questionnaire)


@sdk.operation(["POST"], ["QuestionnaireResponse", "$constraint-check"])
@sdk.operation(["POST"], ["fhir", "QuestionnaireResponse", "$constraint-check"])
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
@sdk.operation(["POST"], ["fhir", "Questionnaire", "$context"])
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
@sdk.operation(["POST"], ["fhir", "Questionnaire", "$extract"])
async def extract_questionnaire_operation(operation, request):
    is_fhir = operation["request"][1] == "fhir"
    resource = request["resource"]
    client = request["app"]["client"]
    jute_service = request["app"]["settings"].JUTE_SERVICE

    run_on_behalf_of_root = False
    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        questionnaire_response = resource
        questionnaire = (
            await client.resources("Questionnaire").search(_id=resource["questionnaire"]).get()
        )
        run_on_behalf_of_root = questionnaire.get("runOnBehalfOfRoot")
    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request["resource"])
        questionnaire_data = env.get("Questionnaire")
        questionnaire = (
            (await client.execute("$to-format/aidbox", data=questionnaire_data))["resource"]
            if is_fhir
            else questionnaire_data
        )
        questionnaire_response = env.get("QuestionnaireResponse")
        run_on_behalf_of_root = questionnaire.get("runOnBehalfOfRoot")

    mappings = [
        await client.resources("Mapping").search(_id=m["id"]).get()
        for m in questionnaire.get("mapping", [])
    ]
    client = request["app"]["client"] if run_on_behalf_of_root else get_user_sdk_client(request)

    context = {
        "Questionnaire": questionnaire,
        "QuestionnaireResponse": questionnaire_response,
        **env,
    }

    await constraint_check(get_aidbox_fhir_client(client) if is_fhir else client, context)
    extraction_result = await extract(client, mappings, context, jute_service)
    return web.json_response(extraction_result)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
@sdk.operation(["POST"], ["fhir", "Questionnaire", {"name": "id"}, "$extract"])
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
@sdk.operation(["POST"], ["fhir", "Questionnaire", "$populate"])
async def populate_questionnaire(operation, request):
    is_fhir = operation["request"][1] == "fhir"
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

    if is_fhir:
        converted = await client.execute("$to-format/aidbox", data=questionnaire_data)
        questionnaire = client.resource("Questionnaire", **converted["resource"])
    else:
        questionnaire = client.resource("Questionnaire", **questionnaire_data)

    client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)

    populated_resource = await populate(
        get_aidbox_fhir_client(client) if is_fhir else client, questionnaire, env
    )
    if is_fhir:
        populated_resource = (await client.execute("$to-format/fhir", data=populated_resource))[
            "resource"
        ]
    return web.json_response(populated_resource)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
@sdk.operation(["POST"], ["fhir", "Questionnaire", {"name": "id"}, "$populate"])
async def populate_questionnaire_instance(operation, request):
    is_fhir = operation["request"][1] == "fhir"
    client = request["app"]["client"]
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request["route-params"]["id"]).get()
    )
    env = parameter_to_env(request["resource"])
    env["Questionnaire"] = questionnaire
    client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)

    populated_resource = await populate(
        get_aidbox_fhir_client(client) if is_fhir else client, questionnaire, env
    )
    if is_fhir:
        populated_resource = (await client.execute("$to-format/fhir", data=populated_resource))[
            "resource"
        ]
    return web.json_response(populated_resource)


@sdk.operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
@sdk.operation(["POST"], ["fhir", "Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return web.json_response(resolve_expression(request["resource"]))
