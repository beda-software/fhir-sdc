from fhirpathpy import evaluate as fhirpath
from fhirpy.base.exceptions import OperationOutcome
from funcy import is_list

from .utils import get_type, load_source_queries, validate_context


async def populate(client, questionnaire, env):
    if "launchContext" in questionnaire:
        validate_context(questionnaire["launchContext"], env)

    await load_source_queries(client, questionnaire, env)

    root = {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": questionnaire.get("id"),
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

    if item["type"] == "group" and item.get("repeats", False) is True and is_list(context):
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
                if type == "Reference":
                    answers.extend([{"value": {"Reference": {"reference": d}}} for d in data])
                else:
                    answers.extend([{"value": {type: d}} for d in data])
        if answers:
            root_item["answer"] = answers
    elif "initialExpression" in item:
        answers = []
        try:
            data = fhirpath(context, item["initialExpression"]["expression"], env)
        except Exception as e:
            raise OperationOutcome(f'Error: "{item["initialExpression"]["expression"]}" - {str(e)}')
        if data and len(data):
            type = get_type(item, data)
            if type == "Reference":
                if item.get("repeats") is True:
                    answers = [{"value": {"Reference": {"reference": d}}} for d in data]
                else:
                    answers = [{"value": {"Reference": {"reference": data[0]}}}]
            else:
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
