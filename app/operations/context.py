from aiohttp import web
from fhirpy.base.exceptions import OperationOutcome

from app.sdk import sdk

from .utils import get_user_sdk_client, load_source_queries, parameter_to_env


@sdk.operation(["POST"], ["Questionnaire", "$context"])
async def get_questionnaire_context(_operation, request):
    client = request["app"]["client"]
    try:
        env = parameter_to_env(request["resource"])
    except Exception as e:
        raise OperationOutcome(str(e))

    try:
        questionnaire_data = env["Questionnaire"]
    except Exception as e:
        error = "`Questionnaire` parameter is required" if str(e) == "'Questionnaire'" else str(e)
        raise OperationOutcome(error)

    questionnaire = client.resource("Questionnaire", **questionnaire_data)

    client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)

    await load_source_queries(client, questionnaire, env)
    return web.json_response(env)
