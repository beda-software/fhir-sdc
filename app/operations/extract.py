from aiohttp import web
from fhirpy.base.exceptions import OperationOutcome

from app.sdk import sdk

from .utils import parameter_to_env


@sdk.operation(["POST"], ["Questionnaire", "$extract"])
async def extract_questionnaire(operation, request):
    resource = request["resource"]

    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = sdk.client.resource(
            "QuestionnaireResponse", **request["resource"]
        )
        questionnaire = (
            await sdk.client.resources("Questionnaire")
            .search(id=questionnaire_response["questionnaire"])
            .get()
        )
    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request["resource"])
        questionnaire = sdk.client.resource("Questionnaire", **env["questionnaire"])
        questionnaire_response = sdk.client.resource(
            "QuestionnaireResponse", **env["questionnaire_response"]
        )

    else:
        questionnaire = sdk.client.resource("Questionnaire", **env["questionnaire"])
        raise OperationOutcome("Wrong parameters")
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
    for mapper in questionnaire.get("mapping", []):
        resp.append(
            await sdk.client.resource("Mapping", id=mapper.id).execute(
                "$apply", data=questionnaire_response
            )
        )

    return web.json_response(resp)
