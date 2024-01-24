import json

from aiohttp import web
from fhirpy.lib import AsyncFHIRClient

from app.converter.fce_to_fhir import from_first_class_extension
from app.converter.fhir_to_fce import to_first_class_extension
from app.sdc.exception import ConstraintCheckOperationOutcome

from ..sdc import (
    assemble,
    constraint_check,
    extract,
    get_questionnaire_context,
    populate,
    resolve_expression,
)
from ..sdc.utils import parameter_to_env, validate_context
from ..utils import get_extract_services

routes = web.RouteTableDef()


@routes.get("/Questionnaire/{id}/$assemble")
async def assemble_handler(request: web.BaseRequest):
    client: AsyncFHIRClient = request.app["client"]
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request.match_info["id"]).get()
    )

    assembled_questionnaire_lazy = await assemble(client, to_first_class_extension(questionnaire))
    assembled_questionnaire = json.loads(json.dumps(assembled_questionnaire_lazy, default=list))

    return web.json_response(from_first_class_extension(assembled_questionnaire))


@routes.post("/QuestionnaireResponse/$constraint-check")
async def constraint_check_handler(request: web.BaseRequest):
    env = parameter_to_env(await request.json())
    env["Questionnaire"] = to_first_class_extension(env["Questionnaire"])
    env["QuestionnaireResponse"] = to_first_class_extension(env["QuestionnaireResponse"])
    client = request.app["client"]

    return web.json_response(await constraint_check(client, env))


@routes.post("/Questionnaire/$context")
async def get_questionnaire_context_handler(request: web.BaseRequest):
    client = request["app"]["client"]
    env = parameter_to_env(await request.json())
    client = request.app["client"]

    return web.json_response(await get_questionnaire_context(client, env))


@routes.post("/Questionnaire/$extract")
async def extract_questionnaire_handler(request: web.BaseRequest):
    resource = await request.json()
    client = request.app["client"]

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
        structure_map_id = structure_map_extension["valueCanonical"].split("/")[-1]
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
        "Questionnaire": to_first_class_extension(questionnaire),
        "QuestionnaireResponse": to_first_class_extension(questionnaire_response),
        **env,
    }

    await constraint_check(client, context)
    extraction_result = await extract(
        client, jute_templates, context, get_extract_services(request.app)
    )
    return web.json_response(extraction_result)


@routes.post("/Questionnaire/{id}/$extract")
async def extract_questionnaire_instance_operation(request: web.BaseRequest):
    resource = await request.json()
    client = request.app["client"]
    fhir_questionnaire = (
        await client.resources("Questionnaire").search(_id=request.match_info["id"]).get()
    )
    jute_templates = []
    structure_map_extensions = [
        ext
        for ext in fhir_questionnaire["extension"]
        if ext["url"]
        == "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap"
    ]

    questionnaire = to_first_class_extension(fhir_questionnaire)

    for structure_map_extension in structure_map_extensions:
        structure_map_id = structure_map_extension["valueCanonical"].split("/")[-1]
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

    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = client.resource("QuestionnaireResponse", **resource)
        context = {
            "Questionnaire": to_first_class_extension(questionnaire),
            "QuestionnaireResponse": questionnaire_response,
        }
        await constraint_check(client, context)
        return web.json_response(
            await extract(client, jute_templates, context, get_extract_services(request.app))
        )

    if resource["resourceType"] == "Parameters":
        env = parameter_to_env(resource)

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
        if "launchContext" in questionnaire:
            validate_context(questionnaire["launchContext"], env)
        context = {
            "QuestionnaireResponse": questionnaire_response,
            "Questionnaire": questionnaire,
            **env,
        }
        await constraint_check(client, context)
        return web.json_response(
            await extract(client, jute_templates, context, get_extract_services(request.app))
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
    client = request.app["client"]
    env = parameter_to_env(await request.json())
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

    questionnaire = to_first_class_extension(questionnaire_data)
    populated_resource = await populate(client, questionnaire, env)
    populated_resource = from_first_class_extension(populated_resource)
    return web.json_response(populated_resource)


@routes.post("/Questionnaire/{id}/$populate")
async def populate_questionnaire_instance(_operation, request: web.BaseRequest):
    client = request.app["client"]
    questionnaire = (
        await client.resources("Questionnaire").search(_id=request.match_info["id"]).get()
    )
    env = parameter_to_env(request["resource"])
    converted = to_first_class_extension(questionnaire)
    env["Questionnaire"] = converted
    populated_resource = await populate(client, converted, env)
    populated_resource = from_first_class_extension(populated_resource)

    return web.json_response(populated_resource)


@routes.post("/Questionnaire/$resolve-expression")
async def resolve_expression_operation_handler(request: web.BaseRequest):
    return web.json_response(resolve_expression(await request.json()))
