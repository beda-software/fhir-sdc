from aiohttp import web

from app.sdk import sdk

from .utils import load_source_queries, parameter_to_env, OperationOutcome


@sdk.operation(["POST"], ["Questionnaire", "$context"])
async def get_questionnaire_context(operation, request):
    try:
        env = parameter_to_env(request["resource"])
    except Exception as e:
        raise OperationOutcome(reason=str(e), status_code=422)

    try:
        questionnaire_data = env["Questionnaire"]
    except Exception as e:
        error = "`Questionnaire` parameter is required" if str(e) == "'Questionnaire'" else str(e)
        raise OperationOutcome(reason=error, status_code=422)

    questionnaire = sdk.client.resource("Questionnaire", **questionnaire_data)
    await load_source_queries(sdk, questionnaire, env)
    return web.json_response(env)
