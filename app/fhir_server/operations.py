import json

from aiohttp import web
from fhirpy.lib import AsyncFHIRClient

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

routes = web.RouteTableDef()


@routes.get("/Questionnaire/{id}/$assemble")
async def assemble_handler(request):
    client: AsyncFHIRClient = request["app"]["client"]
    client.extra_headers = request["headers"]["Authorization"]
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request.match_info["id"]).get()
    )

    assembled_questionnaire_lazy = await assemble(client, questionnaire)
    assembled_questionnaire = json.loads(json.dumps(assembled_questionnaire_lazy, default=list))

    return web.json_response(assembled_questionnaire)


@routes.post("/QuestionnaireResponse/$constraint-check")
async def constraint_check_handler(request):
    env = parameter_to_env(await request.json())
    client = request["app"]["client"]
    client.extra_headers = request["headers"]["Authorization"]

    return web.json_response(await constraint_check(client, env))


@routes.post("/Questionnaire/$context")
async def get_questionnaire_context_handler(request):
    client = request["app"]["client"]
    env = parameter_to_env(await request.json())
    client = request["app"]["client"]
    client.extra_headers = request["headers"]["Authorization"]

    return web.json_response(await get_questionnaire_context(client, env))


@routes.post("/Questionnaire/$extract")
async def extract_questionnaire_handler(request):
    resource = await request.json()
    client = request["app"]["client"]
    client.extra_headers = request["headers"]["Authorization"]
    jute_service = request["app"]["settings"].JUTE_SERVICE

    if resource["resourceType"] == "QuestionnaireResponse":
        env = {}
        questionnaire_response = resource
        questionnaire = (
            await client.resources("Questionnaire").search(_id=resource["questionnaire"]).get()
        )
    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(resource)
        # TODO: Use FHIR spec questionnaire
        questionnaire = env.get("Questionnaire")
        questionnaire_response = env.get("QuestionnaireResponse")

    structure_map_extensions = [
        ext
        for ext in questionnaire["extension"]
        if ext["url"]
        == "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap"
    ]
    jute_templates = []

    for structure_map_extension in structure_map_extensions:
        structure_map_id = structure_map_extension["valueCanonical"].splt("/")[-1]
        structure_map = await client.resources("StructureMap").search(_id=structure_map_id).get()
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
        jute_templates.append(json.loads(template_string))

    context = {
        "Questionnaire": questionnaire,
        "QuestionnaireResponse": questionnaire_response,
        **env,
    }

    await constraint_check(client, context)
    extraction_result = await extract(client, jute_templates, context, jute_service)
    return web.json_response(extraction_result)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
@sdk.operation(["POST"], ["fhir", "Questionnaire", {"name": "id"}, "$extract"])
async def extract_questionnaire_instance_operation(request):
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
        populated_resource = from_first_class_extension(populated_resource)
    return web.json_response(populated_resource)


@sdk.operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
@sdk.operation(["POST"], ["fhir", "Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return web.json_response(resolve_expression(request["resource"]))
