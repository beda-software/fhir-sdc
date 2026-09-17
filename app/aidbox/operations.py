import simplejson as json
from aiohttp import web

from app.sdc.getters import get_questionnaire_mapper

from ..sdc import (
    assemble,
    build_extract_output,
    constraint_check,
    extract,
    get_questionnaire_context,
    populate,
    resolve_expression,
)
from ..sdc.exception import MissingParamOperationOutcome
from ..sdc.utils import (
    build_legacy_extract_input,
    find_parameter_resource,
    get_external_fhir_base_url_from_resource,
    is_sdc_api,
    parameter_to_env,
    resolve_questionnaire,
)
from ..utils import get_extract_services
from .settings import settings
from .utils import AidboxSdcRequest, aidbox_operation, get_user_sdk_client, prepare_args


@aidbox_operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
@prepare_args
async def assemble_op(request: AidboxSdcRequest):
    fhir_questionnaire = (
        await request.fhir_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )

    assembled_questionnaire_lazy = await assemble(request.fhir_client, dict(fhir_questionnaire))
    assembled_questionnaire = json.loads(json.dumps(assembled_questionnaire_lazy, default=list))
    return web.json_response(assembled_questionnaire, dumps=json.dumps)


@aidbox_operation(["POST"], ["QuestionnaireResponse", "$constraint-check"])
@prepare_args
async def constraint_check_operation(request: AidboxSdcRequest):
    client = get_user_sdk_client(
        request.request,
        request.client,
        get_external_fhir_base_url_from_resource(request.resource),
    )
    env = await parameter_to_env(client, request.resource)

    return web.json_response(
        await constraint_check(
            client,
            env["Questionnaire"],
            env,
            legacy_behavior=settings.CONSTRAINT_LEGACY_BEHAVIOR,
        ),
        dumps=json.dumps,
    )


@aidbox_operation(["POST"], ["Questionnaire", "$context"])
@prepare_args
async def get_questionnaire_context_operation(request: AidboxSdcRequest):
    client = get_user_sdk_client(
        request.request,
        request.client,
        get_external_fhir_base_url_from_resource(request.resource),
    )
    env = await parameter_to_env(client, request.resource)

    result = await get_questionnaire_context(client, env["Questionnaire"], env)

    return web.json_response(result, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", "$extract"])
@prepare_args
async def extract_questionnaire_operation(request: AidboxSdcRequest):
    resource = request.resource
    extract_client = get_user_sdk_client(
        request.request,
        request.client,
        get_external_fhir_base_url_from_resource(resource),
    )
    # From Parameters, extract_questionnaire_instance takes the Questionnaire out of the env.
    questionnaire = None
    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire = dict(
            await resolve_questionnaire(request.fhir_client, resource.get("questionnaire"))
        )

    return web.json_response(
        await extract_questionnaire_instance(
            request.fhir_client,
            extract_client,
            questionnaire,
            resource,
            get_extract_services(request.request["app"]),
        ),
        dumps=json.dumps,
    )


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
@prepare_args
async def extract_questionnaire_instance_operation(request: AidboxSdcRequest):
    resource = request.resource
    extract_client = get_user_sdk_client(
        request.request,
        request.client,
        get_external_fhir_base_url_from_resource(resource),
    )
    questionnaire = (
        await request.fhir_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )

    return web.json_response(
        await extract_questionnaire_instance(
            request.fhir_client,
            extract_client,
            dict(questionnaire),
            resource,
            get_extract_services(request.request["app"]),
        ),
        dumps=json.dumps,
    )


async def extract_questionnaire_instance(
    fhir_client,
    extract_client,
    questionnaire,
    resource,
    extract_services,
    *,
    execute=True,
):
    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        env_questionnaire_response = extract_client.resource("QuestionnaireResponse", **resource)
    elif resource["resourceType"] == "Parameters":
        env = await parameter_to_env(extract_client, resource)
        if "QuestionnaireResponse" not in env:
            raise MissingParamOperationOutcome("`QuestionnaireResponse` parameter is required")

        env_questionnaire_response = env["QuestionnaireResponse"]
        questionnaire = questionnaire or env.get("Questionnaire")
    else:
        raise MissingParamOperationOutcome(
            "Either `QuestionnaireResponse` resource or Parameters containing  QuestionnaireResponse are required",
        )

    if questionnaire is None:
        raise MissingParamOperationOutcome("`Questionnaire` parameter is required")

    context = {
        "QuestionnaireResponse": env_questionnaire_response,
        "Questionnaire": questionnaire,
        **env,
    }
    mapper_refs = get_questionnaire_mapper(questionnaire.get("extension", []))
    mappings = [
        await fhir_client.resources("Mapping").search(_id=ref["reference"].split("/")[-1]).get()
        for ref in mapper_refs
    ]
    await constraint_check(
        extract_client,
        questionnaire,
        context,
        legacy_behavior=settings.CONSTRAINT_LEGACY_BEHAVIOR,
        extract_source_queries_legacy_behavior=settings.EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR,
    )

    return await extract(extract_client, mappings, context, extract_services, execute=execute)


@aidbox_operation(["POST"], ["QuestionnaireResponse", "$extract"])
@prepare_args
async def extract_questionnaire_response_operation(request: AidboxSdcRequest):
    parameters = request.resource or {}
    questionnaire_response = find_parameter_resource(parameters, "questionnaire-response")
    if questionnaire_response is None:
        raise MissingParamOperationOutcome("`questionnaire-response` parameter is required")

    return web.json_response(
        await extract_questionnaire_response(request, parameters, questionnaire_response),
        dumps=json.dumps,
    )


@aidbox_operation(["POST"], ["QuestionnaireResponse", {"name": "id"}, "$extract"])
@prepare_args
async def extract_questionnaire_response_instance_operation(request: AidboxSdcRequest):
    questionnaire_response = (
        await request.fhir_client.resources("QuestionnaireResponse")
        .search(_id=request.route_params["id"])
        .get()
    )
    return web.json_response(
        await extract_questionnaire_response(
            request, request.resource or {}, dict(questionnaire_response)
        ),
        dumps=json.dumps,
    )


async def extract_questionnaire_response(
    request: AidboxSdcRequest, parameters: dict, questionnaire_response: dict
):
    """SDC `$extract`: the bundle is returned for the client to submit, where Questionnaire/$extract runs it.

    Deviates where fhir-sdc does: `return` is a batch if a mapper builds one, and warnings refuse too.
    """
    questionnaire = find_parameter_resource(parameters, "questionnaire") or dict(
        await resolve_questionnaire(
            request.fhir_client, questionnaire_response.get("questionnaire")
        )
    )
    extract_client = get_user_sdk_client(
        request.request,
        request.client,
        get_external_fhir_base_url_from_resource(parameters),
    )
    bundles = await extract_questionnaire_instance(
        request.fhir_client,
        extract_client,
        questionnaire,
        build_legacy_extract_input(parameters, questionnaire_response),
        get_extract_services(request.request["app"]),
        execute=False,
    )
    return build_extract_output(bundles)


@aidbox_operation(["POST"], ["Questionnaire", "$populate"])
@prepare_args
async def populate_questionnaire(request: AidboxSdcRequest):
    client = get_user_sdk_client(
        request.request,
        request.client,
        get_external_fhir_base_url_from_resource(request.resource),
    )
    env = await parameter_to_env(client, request.resource)

    if "Questionnaire" not in env:
        raise MissingParamOperationOutcome("`Questionnaire` parameter is required")

    populated_qr = await populate(
        client, env["Questionnaire"], env, sdc_api=is_sdc_api(request.resource)
    )
    return web.json_response(populated_qr, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
@prepare_args
async def populate_questionnaire_instance(request: AidboxSdcRequest):
    client = get_user_sdk_client(
        request.request,
        request.client,
        get_external_fhir_base_url_from_resource(request.resource),
    )
    fhir_questionnaire = (
        await request.fhir_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )

    env = await parameter_to_env(client, request.resource)
    env["Questionnaire"] = fhir_questionnaire

    populated_qr = await populate(
        client, env["Questionnaire"], env, sdc_api=is_sdc_api(request.resource)
    )

    return web.json_response(populated_qr, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return web.json_response(resolve_expression(request["resource"]), dumps=json.dumps)
