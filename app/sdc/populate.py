import logging
from typing import Any

from fhirpy import AsyncFHIRClient
from funcy import is_list

from .context import load_questionnaire_context
from .getters import (
    get_choice_column_paths,
    get_initial_expression,
    get_item_context,
    get_item_population_context,
    get_variable,
)
from .utils import get_type, make_value_key, normalize_answer_value, resolve_expression

logger = logging.getLogger(__name__)


async def populate(
    client: AsyncFHIRClient,
    fhir_questionnaire: dict,
    variables: dict[str, Any],
    *,
    sdc_api: bool = False,
) -> dict:
    populated_response = {
        "resourceType": "QuestionnaireResponse",
        "status": "in-progress",
        "questionnaire": fhir_questionnaire.get("id"),
        "item": [],
    }
    env = await load_questionnaire_context(
        client, fhir_questionnaire, populated_response, variables
    )
    exts = fhir_questionnaire.get("extension", [])
    for variable in get_variable(exts):
        env[variable["name"]] = await resolve_expression(
            client, {}, variable, env, f"variable.{variable['name']}"
        )

    for item in fhir_questionnaire["item"]:
        populated_response["item"].extend(await _handle_item(client, item, env, {}))

    if sdc_api:
        return {
            "resourceType": "Parameters",
            "parameter": [{"name": "response", "resource": populated_response}],
        }
    return populated_response


async def _handle_item(client, item, env, context):
    # Make a copy of the env to populate with variables for nested items
    env = env.copy()

    env["qitem"] = item

    def init_item():
        new_item = {"linkId": item["linkId"]}
        if "text" in item:
            new_item["text"] = item["text"]
        return new_item

    item_exts = item.get("extension", [])
    for variable in get_variable(item_exts):
        env[variable["name"]] = await resolve_expression(
            client,
            context,
            variable,
            env,
            f"{item['linkId']}.variable.{variable['name']}",
        )

    item_context = get_item_context(item_exts)
    if item_context:  # pragma: no cover
        logger.warning("itemContext is deprecated, use itemPopulationContext instead")
        context = await resolve_expression(
            client, context, item_context, env, f"{item['linkId']}.itemContext"
        )

    item_population_context = get_item_population_context(item_exts)
    if item_population_context:
        context = await resolve_expression(
            client,
            context,
            item_population_context,
            env,
            f"{item['linkId']}.itemPopulationContext",
        )
        if "name" in item_population_context:
            env[item_population_context["name"]] = context

    is_repeating = item.get("repeats", False) is True

    if item["type"] == "group" and is_repeating and is_list(context):
        root_items = []

        for c in context:
            if item_population_context and "name" in item_population_context:
                env[item_population_context["name"]] = c
            populated_items = []
            for subitem in item["item"]:
                populated_items.extend(await _handle_item(client, subitem, env, c))
            root_item = init_item()
            root_item["item"] = populated_items

            root_items.append(root_item)
        return root_items

    root_item = init_item()

    initial_expression = get_initial_expression(item_exts)
    if initial_expression:
        answers = []
        data = await resolve_expression(
            client,
            context,
            initial_expression,
            env,
            f"{item['linkId']}.initialExpression",
        )
        if data:
            type_ = get_type(item, data)
            display_path = next(iter(get_choice_column_paths(item_exts)), None)
            if is_repeating:
                answers = [
                    {make_value_key(type_): normalize_answer_value(type_, d, display_path)}
                    for d in data
                ]
            else:
                answers = [
                    {make_value_key(type_): normalize_answer_value(type_, data[0], display_path)}
                ]
        if answers:
            root_item["answer"] = answers
    elif "initial" in item:
        root_item["answer"] = item["initial"]

    if "item" in item:
        populated_items = []
        for subitem in item["item"]:
            populated_items.extend(await _handle_item(client, subitem, env, context))

        root_item["item"] = populated_items

    return [root_item]
