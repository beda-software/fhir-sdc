from aiohttp import web
from fhirpathpy import evaluate as fhirpath
from funcy import is_list

from app.sdk import sdk

from .utils import get_type, parameter_to_env, prepare_bundle


@sdk.operation(["POST"], ["Questionnaire", "$populate"])
async def populate_questionnaire(operation, request):
    env = parameter_to_env(request["resource"])
    questionnaire = sdk.client.resource("Questionnaire", **env["questionnaire"])

    return await populate(questionnaire, env)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
async def populate_questionnaire_instance(operation, request):
    questionnaire = await sdk.client.resources("Questionnaire").get(
        id=request["route-params"]["id"]
    )
    return await populate(questionnaire, parameter_to_env(request["resource"]))


async def populate(questionnaire, env):
    contained = {
        f"{item.resourceType}#{item.id}": item
        for item in questionnaire.get("contained", [])
    }

    for source_query in questionnaire.get("sourceQueries", []):
        if "localRef" in source_query:
            raw_bundle = contained[source_query["localRef"]]
            if raw_bundle:
                bundle = prepare_bundle(raw_bundle, env)
                env[bundle.id] = await sdk.client.execute("/", data=bundle)

    root = {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": questionnaire.id,
        "item": [],
    }
    for item in questionnaire["item"]:
        root["item"].append(handle_item(item, env, {}))

    return web.json_response(root)


def handle_item(item, env, context):
    root = {"linkId": item["linkId"]}
    if "text" in item:
        root["text"] = item["text"]
    if "itemContext" in item:
        data = fhirpath(context, item["itemContext"]["expression"], env)
        context = data
    if (
        context
        and "initialExpression" in item
        and "repeats" in item
        and item["repeats"] is True
    ):
        answers = []
        root["answer"] = answers
        for index, _item in enumerate(context):
            type = get_type(item)
            data = fhirpath(
                context,
                "%context[{}].{}".format(
                    index, item["initialExpression"]["expression"]
                ),
                env,
            )
            answers.append({"value": {item["type"]: data[0]}})
    elif "initialExpression" in item:
        data = fhirpath(context, item["initialExpression"]["expression"], env)
        if data and len(data):
            type = get_type(item)
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
