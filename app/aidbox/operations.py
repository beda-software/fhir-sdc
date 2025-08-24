import simplejson as json
from aiohttp import web

from app.converter.aidbox import from_first_class_extension, to_first_class_extension

from ..sdc import (
    assemble,
    constraint_check,
    extract,
    get_questionnaire_context,
    populate,
    resolve_expression,
)
from ..sdc.exception import MissingParamOperationOutcome
from ..sdc.utils import parameter_to_env, validate_context
from ..utils import get_extract_services
from .utils import AidboxSdcRequest, aidbox_operation, get_user_sdk_client, prepare_args


@aidbox_operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
@prepare_args
async def assemble_op(request: AidboxSdcRequest):
    def get_to_first_class_extension(fhir_resource):
        return to_first_class_extension(fhir_resource, request.aidbox_client)

    fhir_questionnaire = (
        await request.fhir_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )
    fce_questionnaire = await get_to_first_class_extension(fhir_questionnaire)

    assembled_questionnaire_lazy = await assemble(
        request.fhir_client, fce_questionnaire, get_to_first_class_extension
    )
    assembled_questionnaire = json.loads(
        json.dumps(assembled_questionnaire_lazy, default=list)
    )
    if request.is_fhir:
        assembled_questionnaire = await from_first_class_extension(
            assembled_questionnaire, request.aidbox_client
        )
    return web.json_response(assembled_questionnaire, dumps=json.dumps)


@aidbox_operation(["POST"], ["QuestionnaireResponse", "$constraint-check"])
@prepare_args
async def constraint_check_operation(request: AidboxSdcRequest):
    env = parameter_to_env(request.resource)

    fce_questionnaire = (
        await to_first_class_extension(env["Questionnaire"], request.aidbox_client)
        if request.is_fhir
        else env["Questionnaire"]
    )
    client = get_user_sdk_client(request.request, request.client)

    return web.json_response(
        await constraint_check(
            client,
            fce_questionnaire,
            env,
        ),
        dumps=json.dumps,
    )


@aidbox_operation(["POST"], ["Questionnaire", "$context"])
@prepare_args
async def get_questionnaire_context_operation(request: AidboxSdcRequest):
    env = parameter_to_env(request.resource)

    fce_questionnaire = (
        await to_first_class_extension(env["Questionnaire"], request.aidbox_client)
        if request.is_fhir
        else env["Questionnaire"]
    )
    client = get_user_sdk_client(request.request, request.client)
    result = await get_questionnaire_context(client, fce_questionnaire, env)

    return web.json_response(result, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", "$extract"])
@prepare_args
async def extract_questionnaire_operation(request: AidboxSdcRequest):
    resource = request.resource
    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        env_questionnaire_response = resource
        fhir_questionnaire = (
            await request.fhir_client.resources("Questionnaire")
            .search(_id=resource["questionnaire"])
            .get()
        )
        fce_questionnaire = await to_first_class_extension(
            fhir_questionnaire, request.aidbox_client
        )
        env_questionnaire = fhir_questionnaire if request.is_fhir else fce_questionnaire
    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request.resource)
        if "Questionnaire" not in env:
            raise MissingParamOperationOutcome("`Questionnaire` parameter is required")
        if "QuestionnaireResponse" not in env:
            raise MissingParamOperationOutcome(
                "`QuestionnaireResponse` parameter is required"
            )

        fce_questionnaire = (
            await to_first_class_extension(env["Questionnaire"], request.aidbox_client)
            if request.is_fhir
            else env["Questionnaire"]
        )
        env_questionnaire = env["Questionnaire"]
        env_questionnaire_response = env["QuestionnaireResponse"]

    mappings = [
        await request.aidbox_client.resources("Mapping").search(_id=m["id"]).get()
        for m in fce_questionnaire.get("mapping", [])
    ]

    context = {
        "Questionnaire": env_questionnaire,
        "QuestionnaireResponse": env_questionnaire_response,
        **env,
    }

    client = get_user_sdk_client(request.request, request.client)
    await constraint_check(
        client,
        fce_questionnaire,
        context,
    )
    extraction_result = await extract(
        client, mappings, context, get_extract_services(request.request["app"])
    )
    return web.json_response(extraction_result, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
@prepare_args
async def extract_questionnaire_instance_operation(request: AidboxSdcRequest):
    resource = request.resource
    fce_questionnaire = (
        await request.aidbox_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )
    env_questionnaire = (
        await from_first_class_extension(fce_questionnaire, request.aidbox_client)
        if request.is_fhir
        else fce_questionnaire
    )
    extract_client = get_user_sdk_client(request.request, request.client)
    return web.json_response(
        await extract_questionnaire_instance(
            request.aidbox_client,
            extract_client,
            fce_questionnaire,
            env_questionnaire,
            resource,
            get_extract_services(request.request["app"]),
        ),
        dumps=json.dumps,
    )


async def extract_questionnaire_instance(
    aidbox_client,
    extract_client,
    fce_questionnaire,
    env_questionnaire,
    resource,
    extract_services,
):
    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        env_questionnaire_response = extract_client.resource(
            "QuestionnaireResponse", **resource
        )
    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(resource)
        if "QuestionnaireResponse" not in env:
            raise MissingParamOperationOutcome(
                "`QuestionnaireResponse` parameter is required"
            )

        env_questionnaire_response = env["QuestionnaireResponse"]
    else:
        raise MissingParamOperationOutcome(
            "Either `QuestionnaireResponse` resource or Parameters containing  QuestionnaireResponse are required",
        )

    if "launchContext" in fce_questionnaire:
        validate_context(fce_questionnaire["launchContext"], env)
    context = {
        "QuestionnaireResponse": env_questionnaire_response,
        "Questionnaire": env_questionnaire,
        **env,
    }
    mappings = [
        await aidbox_client.resources("Mapping").search(_id=m["id"]).get()
        for m in fce_questionnaire.get("mapping", [])
    ]
    await constraint_check(
        extract_client,
        fce_questionnaire,
        context,
    )

    return await extract(extract_client, mappings, context, extract_services)


@aidbox_operation(["POST"], ["Questionnaire", "$populate"])
@prepare_args
async def populate_questionnaire(request: AidboxSdcRequest):
    env = parameter_to_env(request.resource)

    if "Questionnaire" not in env:
        raise MissingParamOperationOutcome("`Questionnaire` parameter is required")

    fce_questionnaire = (
        await to_first_class_extension(env["Questionnaire"], request.aidbox_client)
        if request.is_fhir
        else env["Questionnaire"]
    )
    client = get_user_sdk_client(request.request, request.client)

    fce_populated_qr = await populate(client, fce_questionnaire, env)
    if request.is_fhir:
        fce_populated_qr = await from_first_class_extension(
            fce_populated_qr, request.aidbox_client
        )
    return web.json_response(fce_populated_qr, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
@prepare_args
async def populate_questionnaire_instance(request: AidboxSdcRequest):
    fhir_questionnaire = (
        await request.fhir_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )
    fce_questionnaire = await to_first_class_extension(
        fhir_questionnaire, request.aidbox_client
    )
    env = parameter_to_env(request.resource)
    env["Questionnaire"] = fhir_questionnaire if request.is_fhir else fce_questionnaire
    client = get_user_sdk_client(request.request, request.client)

    fce_populated_qr = await populate(client, fce_questionnaire, env)

    if request.is_fhir:
        fce_populated_qr = await from_first_class_extension(
            fce_populated_qr, request.aidbox_client
        )
    return web.json_response(fce_populated_qr, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return web.json_response(resolve_expression(request["resource"]), dumps=json.dumps)
