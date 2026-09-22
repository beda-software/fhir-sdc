from ..sdc import resolve_expression
from ..sdc.operations import (
    run_assemble,
    run_constraint_check,
    run_context,
    run_extract,
    run_populate,
)
from ..utils import render_json
from .utils import AidboxSdcRequest, aidbox_operation, prepare_args


@aidbox_operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
@prepare_args
async def assemble_op(request: AidboxSdcRequest):
    return render_json(await run_assemble(request.context, request.route_params["id"]))


@aidbox_operation(["POST"], ["QuestionnaireResponse", "$constraint-check"])
@prepare_args
async def constraint_check_operation(request: AidboxSdcRequest):
    return render_json(await run_constraint_check(request.context, request.resource))


@aidbox_operation(["POST"], ["Questionnaire", "$context"])
@prepare_args
async def get_questionnaire_context_operation(request: AidboxSdcRequest):
    return render_json(await run_context(request.context, request.resource))


@aidbox_operation(["POST"], ["Questionnaire", "$extract"])
@prepare_args
async def extract_questionnaire_operation(request: AidboxSdcRequest):
    return render_json(await run_extract(request.context, request.resource))


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
@prepare_args
async def extract_questionnaire_instance_operation(request: AidboxSdcRequest):
    return render_json(
        await run_extract(request.context, request.resource, request.route_params["id"])
    )


@aidbox_operation(["POST"], ["Questionnaire", "$populate"])
@prepare_args
async def populate_questionnaire(request: AidboxSdcRequest):
    return render_json(await run_populate(request.context, request.resource))


@aidbox_operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
@prepare_args
async def populate_questionnaire_instance(request: AidboxSdcRequest):
    return render_json(
        await run_populate(request.context, request.resource, request.route_params["id"])
    )


@aidbox_operation(["POST"], ["Questionnaire", "$resolve-expression"], public=True)
def resolve_expression_operation(_operation, request):
    return render_json(resolve_expression(request["resource"]))
