from aiohttp import web

from app.sdk import sdk

from .utils import load_source_queries


@sdk.operation(["GET"], ["Questionnaire", {"name": "id"}, "$context"])
async def populate_questionnaire_instance(operation, request):
    questionnaire = await sdk.client.resources("Questionnaire").get(
        id=request["route-params"]["id"]
    )
    env = {}
    await load_source_queries(sdk, questionnaire, env)
    return web.json_response(env)
