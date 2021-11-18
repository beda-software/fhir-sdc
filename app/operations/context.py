from aiohttp import web
from fhirpy.base.exceptions import OperationOutcome

from app.sdk import sdk

from .utils import load_source_queries, parameter_to_env, get_user_sdk_client


@sdk.operation(["POST"], ["Questionnaire", "$context"])
async def get_questionnaire_context(_operation, request):
    try:
        env = parameter_to_env(request["resource"])
    except Exception as e:
        raise OperationOutcome(str(e))

    try:
        questionnaire_data = env["Questionnaire"]
    except Exception as e:
        error = "`Questionnaire` parameter is required" if str(e) == "'Questionnaire'" else str(e)
        raise OperationOutcome(error)

    questionnaire = sdk.client.resource("Questionnaire", **questionnaire_data)

    client = sdk.client if questionnaire.get('runOnBehalfOfRoot') else get_user_sdk_client(request)

    await load_source_queries(client, questionnaire, env)
    return web.json_response(env)
