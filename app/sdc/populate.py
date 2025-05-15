from fhirpy.base.exceptions import OperationOutcome
from funcy import is_list

from .utils import get_type, load_source_queries, validate_context
from app.cached_fhirpath import fhirpath


async def populate(client, fce_questionnaire, env):
    if "launchContext" in fce_questionnaire:
        validate_context(fce_questionnaire["launchContext"], env)
    if "QuestionnaireResponse" not in env:
        # Populate operation does not accept QR, but source queries might use it
        # in constraint-check operations
        # This "hack" allows using QuestionnaireResponse as env variable (otherwise fhirpath will fail)
        env["QuestionnaireResponse"] = {
            "resourceType": "QuestionnaireResponse",
            "status": "in-progress",
        }

    await load_source_queries(client, fce_questionnaire, env)

    root = {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": fce_questionnaire.get("id"),
        "item": [],
    }
    for item in fce_questionnaire["item"]:
        root["item"].extend(_handle_item(item, env, {}))

    return root


def _handle_item(item, env, context):
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
                populated_items.extend(_handle_item(i, env, c))
            root_item = init_item()
            root_item["item"] = populated_items

            root_items.append(root_item)
        return root_items

    root_item = init_item()

    if context and "initialExpression" in item and item.get("repeats", False) is True:
        answers = []
        for item_context in context:
            data = fhirpath(
                item_context,
                item["initialExpression"]["expression"],
                env,
            )
            if data and len(data):
                type = get_type(item, data)
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
            populated_items.extend(_handle_item(i, env, context))

        root_item["item"] = populated_items

    return [root_item]
