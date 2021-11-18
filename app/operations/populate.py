from aiohttp import web
from fhirpathpy import evaluate as fhirpath
from funcy import is_list

from app.sdk import sdk

from .utils import get_type, load_source_queries, parameter_to_env, validate_context, get_user_sdk_client


@sdk.operation(["POST"], ["Questionnaire", "$populate"])
async def populate_questionnaire(_operation, request):
    env = parameter_to_env(request["resource"])

    questionnaire_data = env["Questionnaire"]
    if not questionnaire_data:
        # TODO: return OperationOutcome
        return web.json_response(
            {
                "error": "bad_request",
                "error_description": "`Questionnaire` parameter is required",
            },
            status=422,
        )

    questionnaire = sdk.client.resource("Questionnaire", **questionnaire_data)
    client = sdk.client if questionnaire.get('runOnBehalfOfRoot') else get_user_sdk_client(request)

    populated_resource = await populate(client, questionnaire, env)
    return web.json_response(populated_resource)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
async def populate_questionnaire_instance(_operation, request):
    questionnaire = await sdk.client.resources("Questionnaire").get(
        id=request["route-params"]["id"]
    )
    env = parameter_to_env(request["resource"])
    env["Questionnaire"] = questionnaire
    client = sdk.client if questionnaire.get('runOnBehalfOfRoot') else get_user_sdk_client(request)

    populated_resource = await populate(client, questionnaire, env)
    return web.json_response(populated_resource)


async def populate(client, questionnaire, env):
    if "launchContext" in questionnaire:
        validate_context(questionnaire["launchContext"], env)

    await load_source_queries(client, questionnaire, env)

    root = {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": questionnaire.id,
        "item": [],
    }
    for item in questionnaire["item"]:
        root["item"].extend(handle_item(item, env, {}))

    return root


def handle_item(item, env, context):
    def init_item():
        new_item = {"linkId": item["linkId"]}
        if "text" in item:
            new_item["text"] = item["text"]
        return new_item

    if "itemContext" in item:
        context = fhirpath(context, item["itemContext"]["expression"], env)

    if "itemPopulationContext" in item:
        context = fhirpath(context, item["itemPopulationContext"]["expression"], env)

    if (
        item["type"] == "group"
        and item.get("repeats", False) is True
        and is_list(context)
    ):
        root_items = []

        for c in context:
            populated_items = []
            for i in item["item"]:
                populated_items.extend(handle_item(i, env, c))
            root_item = init_item()
            root_item["item"] = populated_items

            root_items.append(root_item)
        return root_items

    root_item = init_item()

    if context and "initialExpression" in item and item.get("repeats", False) is True:
        answers = []
        for index, _item in enumerate(context):
            data = fhirpath(
                context,
                "%context[{}].{}".format(index, item["initialExpression"]["expression"]),
                env,
            )
            if data and len(data):
                type = get_type(item, data)
                answers.extend([{"value": {type: d}} for d in data])
        if answers:
            root_item["answer"] = answers
    elif "initialExpression" in item:
        answers = []
        data = fhirpath(context, item["initialExpression"]["expression"], env)
        if data and len(data):
            type = get_type(item, data)
            if item.get("repeats") is True:
                answers = [{"value": {type: d}} for d in data]
            else:
                answers = [{"value": {type: data[0]}}]
        if answers:
            root_item["answer"] = answers
    elif "initial" in item:
        root_item["answer"] = item["initial"]

    if "item" in item:
        populated_items = []
        for i in item["item"]:
            populated_items.extend(handle_item(i, env, context))

        root_item["item"] = populated_items

    return [root_item]
