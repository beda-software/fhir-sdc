from aiohttp import web

from ..sdc import resolve_expression
from ..sdc.operations import (
    SdcContext,
    run_assemble,
    run_constraint_check,
    run_context,
    run_extract,
    run_populate,
)
from ..utils import build_user_client, get_extract_services, render_json

routes = web.RouteTableDef()


@routes.get("/Questionnaire/{id}/$assemble")
async def assemble_handler(request: web.Request):
    return render_json(await run_assemble(build_sdc_context(request), request.match_info["id"]))


@routes.post("/QuestionnaireResponse/$constraint-check")
async def constraint_check_handler(request: web.Request):
    return render_json(await run_constraint_check(build_sdc_context(request), await request.json()))


@routes.post("/Questionnaire/$context")
async def get_questionnaire_context_handler(request: web.Request):
    return render_json(await run_context(build_sdc_context(request), await request.json()))


@routes.post("/Questionnaire/$extract")
async def extract_questionnaire_handler(request: web.Request):
    return render_json(await run_extract(build_sdc_context(request), await request.json()))


@routes.post("/Questionnaire/{id}/$extract")
async def extract_questionnaire_instance_operation(request: web.Request):
    context = build_sdc_context(request)
    return render_json(await run_extract(context, await request.json(), request.match_info["id"]))


@routes.post("/Questionnaire/$populate")
async def populate_questionnaire_handler(request: web.Request):
    return render_json(await run_populate(build_sdc_context(request), await request.json()))


@routes.post("/Questionnaire/{id}/$populate")
async def populate_questionnaire_instance(request: web.Request):
    context = build_sdc_context(request)
    return render_json(await run_populate(context, await request.json(), request.match_info["id"]))


@routes.post("/Questionnaire/$resolve-expression")
async def resolve_expression_operation_handler(request: web.Request):
    return render_json(resolve_expression(await request.json()))


@routes.get("/healthcheck")
async def healthcheck(request: web.Request):
    return web.json_response({"status": "ok"})


def build_sdc_context(request: web.Request) -> SdcContext:
    user_client = build_user_client(request.headers, request.app["settings"].BASE_URL)
    return SdcContext(user_client, get_extract_services(request.app))
