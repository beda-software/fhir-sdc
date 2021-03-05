from aiohttp import web
from fhirpathpy import evaluate as fhirpath
from funcy import is_list

from app.sdk import sdk

from .utils import get_type, load_source_queries, parameter_to_env, validate_context


@sdk.operation(["POST"], ["Questionnaire", "$populate"])
async def populate_questionnaire(operation, request):
    env = parameter_to_env(request["resource"])

    questionnaire_data = env.get("questionnaire") or env.get("Questionnaire")
    if not questionnaire_data:
        # TODO: return OperationOutcome
        return web.json_response(
            {"error": "bad_request", "error_description": "`Questionnaire` parameter is required",},
            status=422,
        )

    questionnaire = sdk.client.resource("Questionnaire", **questionnaire_data)
    populated_resource = await populate(questionnaire, env)
    return web.json_response(populated_resource)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
async def populate_questionnaire_instance(operation, request):
    questionnaire = await sdk.client.resources("Questionnaire").get(
        id=request["route-params"]["id"]
    )
    populated_resource = await populate(questionnaire, parameter_to_env(request["resource"]))
    return web.json_response(populated_resource)


async def populate(questionnaire, env):

    validate_context(questionnaire["launchContext"], env)

    await load_source_queries(sdk, questionnaire, env)

    root = {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": questionnaire.id,
        "item": [],
    }
    for item in questionnaire["item"]:
        root["item"].append(handle_item(item, env, {}))

    return root


def handle_item(item, env, context):
    root = {"linkId": item["linkId"]}
    if "text" in item:
        root["text"] = item["text"]
    if "itemContext" in item:
        data = fhirpath(context, item["itemContext"]["expression"], env)
        context = data
    if context and "initialExpression" in item and "repeats" in item and item["repeats"] is True:
        answers = []
        root["answer"] = answers
        for index, _item in enumerate(context):
            data = fhirpath(
                context,
                "%context[{}].{}".format(index, item["initialExpression"]["expression"]),
                env,
            )
            if data and len(data):
                type = get_type(item, data)
                answers.append({"value": {type: data[0]}})
    elif "initialExpression" in item:
        data = fhirpath(context, item["initialExpression"]["expression"], env)
        if data and len(data):
            type = get_type(item, data)
            if item.get("repeats") is True:
                root["answer"] = [{"value": {type: d}} for d in data]
            else:
                root["answer"] = [{"value": {type: data[0]}}]
    elif "initial" in item:
        root["answer"] = item["initial"]

    if (
        item["type"] == "group"
        and "repeats" in item
        and item["repeats"] is True
        and is_list(context)
    ):
        answer = []
        for c in context:
            q = []
            for i in item["item"]:
                q.append(handle_item(i, env, c))
            answer.append({"item": q})
        root["answer"] = answer

    elif "item" in item:
        root["item"] = []
        for i in item["item"]:
            root["item"].append(handle_item(i, env, context))

    return root
