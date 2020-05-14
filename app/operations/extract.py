from aiohttp import web

from app.sdk import sdk


@sdk.operation(["POST"], ["Questionnaire", "$extract"])
async def extract_questionnaire(operation, request):
    questionnaire_response = sdk.client.resource(
        "QuestionnaireResponse", **request["resource"]
    )
    questionnaire = (
        await sdk.client.resources("Questionnaire")
        .search(id=questionnaire_response["questionnaire"])
        .get()
    )
    return await extract(questionnaire, questionnaire_response)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
async def extract_questionnaire_instance(operation, request):
    questionnaire_response = sdk.client.resource(
        "QuestionnaireResponse", **request["resource"]
    )
    questionnaire = (
        await sdk.client.resources("Questionnaire")
        .search(id=request["route-params"]["id"])
        .get()
    )
    return await extract(questionnaire, questionnaire_response)


async def extract(questionnaire, questionnaire_response):
    resp = []
    for mapper in questionnaire["mapping"]:
        resp.append(
            await sdk.client.resource("Mapping", id=mapper.id).execute(
                "$apply", data=questionnaire_response
            )
        )

    return web.json_response(resp)
