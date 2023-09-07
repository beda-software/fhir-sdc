import json

from aiohttp import web

from app.converter.fce_to_fhir import from_first_class_extension
from app.converter.fhir_to_fce import to_first_class_extension

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
from ..utils import get_extract_services
from .sdk import sdk
from .utils import get_aidbox_fhir_client, get_organization_client, get_user_sdk_client


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
        assembled_questionnaire = from_first_class_extension(assembled_questionnaire)
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
            to_first_class_extension(questionnaire_data) if is_fhir else questionnaire_data
        )
        questionnaire_response = env.get("QuestionnaireResponse")
        run_on_behalf_of_root = questionnaire.get("runOnBehalfOfRoot")

    mappings = [
        await client.resources("Mapping").search(_id=m["id"]).get()
        for m in questionnaire.get("mapping", [])
    ]

    context = {
        "Questionnaire": questionnaire,
        "QuestionnaireResponse": questionnaire_response,
        **env,
    }

    client = request["app"]["client"] if run_on_behalf_of_root else get_user_sdk_client(request)
    client = get_aidbox_fhir_client(client) if is_fhir else client

    await constraint_check(client, context)
    extraction_result = await extract(
        client, mappings, context, get_extract_services(request["app"])
    )
    return web.json_response(extraction_result)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
@sdk.operation(["POST"], ["fhir", "Questionnaire", {"name": "id"}, "$extract"])
async def extract_questionnaire_instance_operation(operation, request):
    is_fhir = operation["request"][1] == "fhir"
    resource = request["resource"]
    client = request["app"]["client"]
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request["route-params"]["id"]).get()
    )
    client = (
        request["app"]["client"]
        if questionnaire.get("runOnBehalfOfRoot")
        else get_user_sdk_client(request)
    )
    extract_client = get_aidbox_fhir_client(client) if is_fhir else client
    return web.json_response(
        await extract_questionnaire_instance(
            client, extract_client, questionnaire, resource, get_extract_services(request["app"])
        )
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
        converted = to_first_class_extension(questionnaire_data)
        questionnaire = client.resource("Questionnaire", **converted)
    else:
        questionnaire = client.resource("Questionnaire", **questionnaire_data)

    client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)

    populated_resource = await populate(
        get_aidbox_fhir_client(client) if is_fhir else client, questionnaire, env
    )
    if is_fhir:
        populated_resource = from_first_class_extension(populated_resource)
    return web.json_response(populated_resource)


@sdk.operation(
    ["POST"],
    ["Organization", {"name": "org_id"}, "fhir", "Questionnaire", {"name": "id"}, "$populate"],
)
@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
@sdk.operation(["POST"], ["fhir", "Questionnaire", {"name": "id"}, "$populate"])
async def populate_questionnaire_instance(operation, request):
    aidbox_client = request["app"]["client"]
    if operation["request"][1] == "Organization":
        is_fhir = True
        fhir_client = get_organization_client(aidbox_client, request["route-params"]["org_id"])
    else:
        is_fhir = operation["request"][1] == "fhir"
        fhir_client = get_aidbox_fhir_client(aidbox_client)
    questionnaire = (
        await aidbox_client.resources("Questionnaire")
        .search(_id=request["route-params"]["id"])
        .get()
    )
    env = parameter_to_env(request["resource"])
    env["Questionnaire"] = questionnaire
    # TODO handle runOnBehalfOfRoot
    # client = fhir_client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)

    populated_resource = await populate(
        fhir_client if is_fhir else aidbox_client, questionnaire, env
    )
    if is_fhir:
        populated_resource = from_first_class_extension(populated_resource)
    return web.json_response(populated_resource)


@sdk.operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
@sdk.operation(["POST"], ["fhir", "Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return web.json_response(resolve_expression(request["resource"]))
