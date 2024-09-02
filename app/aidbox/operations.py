import json

from aiohttp import web

from app.converter.aidbox import from_first_class_extension, to_first_class_extension

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
from .utils import AidboxSdcRequest, aidbox_operation, get_user_sdk_client, prepare_args


@aidbox_operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
@prepare_args
async def assemble_op(request: AidboxSdcRequest):
    questionnaire = (
        await request.aidbox_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )

    assembled_questionnaire_lazy = await assemble(request.fhir_client, questionnaire)
    assembled_questionnaire = json.loads(json.dumps(assembled_questionnaire_lazy, default=list))
    if request.is_fhir:
        assembled_questionnaire = await from_first_class_extension(
            assembled_questionnaire, request.aidbox_client
        )
    return web.json_response(assembled_questionnaire)


@aidbox_operation(["POST"], ["QuestionnaireResponse", "$constraint-check"])
@prepare_args
async def constraint_check_operation(request: AidboxSdcRequest):
    env = parameter_to_env(request.resource)

    questionnaire = (
        await to_first_class_extension(env["Questionnaire"], request.aidbox_client)
        if request.is_fhir
        else env["Questionnaire"]
    )
    as_root = questionnaire.get("runOnBehalfOfRoot")
    client = client if as_root else get_user_sdk_client(request.request, request.client)

    return web.json_response(await constraint_check(client, env))


@aidbox_operation(["POST"], ["Questionnaire", "$context"])
@prepare_args
async def get_questionnaire_context_operation(request: AidboxSdcRequest):
    env = parameter_to_env(request.resource)

    questionnaire = (
        await to_first_class_extension(env["Questionnaire"], request.aidbox_client)
        if request.is_fhir
        else env["Questionnaire"]
    )
    as_root = questionnaire.get("runOnBehalfOfRoot")
    client = client if as_root else get_user_sdk_client(request.request, request.client)
    result = await get_questionnaire_context(client, env)

    return web.json_response(result)


@aidbox_operation(["POST"], ["Questionnaire", "$extract"])
@prepare_args
async def extract_questionnaire_operation(request: AidboxSdcRequest):
    resource = request.resource

    as_root = False
    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        questionnaire_response = resource
        questionnaire = (
            await request.aidbox_client.resources("Questionnaire")
            .search(_id=resource["questionnaire"])
            .get()
        )
        as_root = questionnaire.get("runOnBehalfOfRoot")
    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request.resource)
        questionnaire = (
            await to_first_class_extension(env["Questionnaire"], request.aidbox_client)
            if request.is_fhir
            else env["Questionnaire"]
        )
        questionnaire_response = env.get("QuestionnaireResponse")
        as_root = questionnaire.get("runOnBehalfOfRoot")

    mappings = [
        await request.aidbox_client.resources("Mapping").search(_id=m["id"]).get()
        for m in questionnaire.get("mapping", [])
    ]

    context = {
        "Questionnaire": questionnaire,
        "QuestionnaireResponse": questionnaire_response,
        **env,
    }

    client = client if as_root else get_user_sdk_client(request.request, request.client)
    await constraint_check(client, context)
    extraction_result = await extract(
        client, mappings, context, get_extract_services(request.request["app"])
    )
    return web.json_response(extraction_result)


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
@prepare_args
async def extract_questionnaire_instance_operation(request: AidboxSdcRequest):
    resource = request.resource
    questionnaire = (
        await request.aidbox_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )
    as_root = questionnaire.get("runOnBehalfOfRoot")
    extract_client = (
        request.client if as_root else get_user_sdk_client(request.request, request.client)
    )
    return web.json_response(
        await extract_questionnaire_instance(
            request.aidbox_client,
            extract_client,
            questionnaire,
            resource,
            get_extract_services(request.request["app"]),
        )
    )


@aidbox_operation(["POST"], ["Questionnaire", "$populate"])
@prepare_args
async def populate_questionnaire(request: AidboxSdcRequest):
    env = parameter_to_env(request.resource)

    if "Questionnaire" not in env:
        # TODO: return OperationOutcome
        return web.json_response(
            {
                "error": "bad_request",
                "error_description": "`Questionnaire` parameter is required",
            },
            status=422,
        )

    questionnaire = (
        await to_first_class_extension(env["Questionnaire"], request.aidbox_client)
        if request.is_fhir
        else env["Questionnaire"]
    )
    as_root = questionnaire.get("runOnBehalfOfRoot")
    client = request.client if as_root else get_user_sdk_client(request.request, request.client)

    populated_resource = await populate(client, questionnaire, env)
    if request.is_fhir:
        populated_resource = await from_first_class_extension(
            populated_resource, request.aidbox_client
        )
    return web.json_response(populated_resource)


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
@prepare_args
async def populate_questionnaire_instance(request: AidboxSdcRequest):
    questionnaire = (
        await request.aidbox_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )
    env = parameter_to_env(request.resource)
    as_root = questionnaire.get("runOnBehalfOfRoot")
    client = client if as_root else get_user_sdk_client(request.request, request.client)

    populated_resource = await populate(client, questionnaire, env)
    if request.is_fhir:
        populated_resource = await from_first_class_extension(
            populated_resource, request.aidbox_client
        )
    return web.json_response(populated_resource)


@aidbox_operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return web.json_response(resolve_expression(request["resource"]))
