import simplejson as json
from aiohttp import web

from app.sdc.getters import get_questionnaire_mapper

from ..sdc import (
    assemble,
    constraint_check,
    extract,
    get_questionnaire_context,
    populate,
    resolve_expression,
)
from ..sdc.exception import MissingParamOperationOutcome
from ..sdc.utils import is_sdc_api, parameter_to_env, resolve_questionnaire
from ..utils import get_extract_services
from .utils import AidboxSdcRequest, aidbox_operation, prepare_args


@aidbox_operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
@prepare_args
async def assemble_op(request: AidboxSdcRequest):
    fhir_questionnaire = (
        await request.user_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )

    assembled_questionnaire_lazy = await assemble(request.user_client, dict(fhir_questionnaire))
    assembled_questionnaire = json.loads(json.dumps(assembled_questionnaire_lazy, default=list))
    return web.json_response(assembled_questionnaire, dumps=json.dumps)


@aidbox_operation(["POST"], ["QuestionnaireResponse", "$constraint-check"])
@prepare_args
async def constraint_check_operation(request: AidboxSdcRequest):
    env = await parameter_to_env(request.data_client, request.resource)

    return web.json_response(
        await constraint_check(
            request.data_client,
            env["Questionnaire"],
            env,
        ),
        dumps=json.dumps,
    )


@aidbox_operation(["POST"], ["Questionnaire", "$context"])
@prepare_args
async def get_questionnaire_context_operation(request: AidboxSdcRequest):
    env = await parameter_to_env(request.data_client, request.resource)

    result = await get_questionnaire_context(request.data_client, env["Questionnaire"], env)

    return web.json_response(result, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", "$extract"])
@prepare_args
async def extract_questionnaire_operation(request: AidboxSdcRequest):
    resource = request.resource
    # From Parameters, extract_questionnaire_instance takes the Questionnaire out of the env.
    questionnaire = None
    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire = dict(
            await resolve_questionnaire(request.user_client, resource.get("questionnaire"))
        )

    return web.json_response(
        await extract_questionnaire_instance(
            request.user_client,
            request.data_client,
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
    questionnaire = (
        await request.user_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )

    return web.json_response(
        await extract_questionnaire_instance(
            request.user_client,
            request.data_client,
            dict(questionnaire),
            resource,
            get_extract_services(request.request["app"]),
        ),
        dumps=json.dumps,
    )


async def extract_questionnaire_instance(
    user_client,
    data_client,
    questionnaire,
    resource,
    extract_services,
):
    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        env_questionnaire_response = data_client.resource("QuestionnaireResponse", **resource)
    elif resource["resourceType"] == "Parameters":
        env = await parameter_to_env(data_client, resource)
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
        await user_client.resources("Mapping").search(_id=ref["reference"].split("/")[-1]).get()
        for ref in mapper_refs
    ]
    await constraint_check(
        data_client,
        questionnaire,
        context,
    )

    return await extract(data_client, mappings, context, extract_services)


@aidbox_operation(["POST"], ["Questionnaire", "$populate"])
@prepare_args
async def populate_questionnaire(request: AidboxSdcRequest):
    env = await parameter_to_env(request.data_client, request.resource)

    if "Questionnaire" not in env:
        raise MissingParamOperationOutcome("`Questionnaire` parameter is required")

    populated_qr = await populate(
        request.data_client, env["Questionnaire"], env, sdc_api=is_sdc_api(request.resource)
    )
    return web.json_response(populated_qr, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
@prepare_args
async def populate_questionnaire_instance(request: AidboxSdcRequest):
    fhir_questionnaire = (
        await request.user_client.resources("Questionnaire")
        .search(_id=request.route_params["id"])
        .get()
    )

    env = await parameter_to_env(request.data_client, request.resource)
    env["Questionnaire"] = fhir_questionnaire

    populated_qr = await populate(
        request.data_client, env["Questionnaire"], env, sdc_api=is_sdc_api(request.resource)
    )

    return web.json_response(populated_qr, dumps=json.dumps)


@aidbox_operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return web.json_response(resolve_expression(request["resource"]), dumps=json.dumps)
