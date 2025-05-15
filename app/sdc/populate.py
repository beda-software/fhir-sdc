import asyncio

from fhirpathpy import evaluate as fhirpath
from fhirpy.base.exceptions import OperationOutcome
from funcy import is_list

from .utils import get_type, load_source_queries, validate_context


def execute_fhirpath(link_id, item_context, expression, env):
    expression_result = fhirpath(item_context, expression, env)
    return {
        "linkId": link_id,
        "expression_result": expression_result,
    }


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

    initial_expressions_map = await get_initial_expressions_map(fce_questionnaire, env, {})

    for item in fce_questionnaire["item"]:
        root["item"].extend(_handle_item(item, env, {}, initial_expressions_map))

    return root


async def get_initial_expressions_map(fce_questionnaire, env, context):
    loop = asyncio.get_running_loop()

    initial_expressions_map = {}

    def get_expressions(fce_questionnaire_item, link_id_coroutines=[]):
        for item in fce_questionnaire_item["item"]:
            if "initialExpression" in item:
                expression = item["initialExpression"]["expression"]

                if context and item.get("repeats", False) is True:
                    for ctx in context:
                        link_id_coroutines.append(
                            {
                                "linkId": item["linkId"],
                                "context": ctx,
                                "expression": expression,
                            }
                        )
                else:
                    link_id_coroutines.append(
                        {
                            "linkId": item["linkId"],
                            "expression": expression,
                        }
                    )

            if "item" in item:
                get_expressions(item, link_id_coroutines)

        return link_id_coroutines

    link_id_expressions = get_expressions(fce_questionnaire)

    results = await asyncio.gather(
        *[
            loop.run_in_executor(
                None,
                execute_fhirpath,
                link_id_expression["linkId"],
                link_id_expression.get("context", context),
                link_id_expression["expression"],
                env,
            )
            for link_id_expression in link_id_expressions
        ]
    )

    for result in results:
        if result["linkId"] not in initial_expressions_map:
            initial_expressions_map[result["linkId"]] = []

        if result["expression_result"] is not None:
            initial_expressions_map[result["linkId"]].append(result["expression_result"])

    return initial_expressions_map


def _handle_item(item, env, context, initial_expressions_map={}):
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
        results = initial_expressions_map.get(item["linkId"], [])
        answers = []
        for data in results:
            if data and len(data):
                type = get_type(item, data)
                answers.extend([{"value": {type: d}} for d in data])
        if answers:
            root_item["answer"] = answers

    elif "initialExpression" in item:
        try:
            data = initial_expressions_map.get(item["linkId"], [])
        except Exception as e:
            raise OperationOutcome(f'Error: "{item["initialExpression"]["expression"]}" - {str(e)}')

        if data and len(data):
            type = get_type(item, data)
            if item.get("repeats") is True:
                root_item["answer"] = [{"value": {type: d}} for d in data]
            else:
                root_item["answer"] = [{"value": {type: data[0]}}]

    elif "initial" in item:
        root_item["answer"] = item["initial"]

    if "item" in item:
        populated_items = []
        for i in item["item"]:
            populated_items.extend(_handle_item(i, env, context))
        root_item["item"] = populated_items

    return [root_item]
