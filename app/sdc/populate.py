import logging

from funcy import is_list

from .getters import (
    get_initial_expression,
    get_item_context,
    get_item_population_context,
    get_launch_context,
    get_variable,
)
from .utils import (
    get_type,
    load_source_queries,
    make_value_key,
    normalize_answer_value,
    resolve_expression,
    validate_context,
)

logger = logging.getLogger(__name__)


async def populate(client, fhir_questionnaire, env):
    exts = fhir_questionnaire.get("extension", [])
    launch_context = get_launch_context(exts)
    if launch_context:
        validate_context(launch_context, env)
    if "QuestionnaireResponse" not in env:
        # Populate operation does not accept QR, but source queries might use it
        # in constraint-check operations
        # This "hack" allows using QuestionnaireResponse as env variable (otherwise fhirpath will fail)
        env["QuestionnaireResponse"] = {
            "resourceType": "QuestionnaireResponse",
            "status": "in-progress",
        }

    await load_source_queries(client, fhir_questionnaire, env)

    root = {
        **env["QuestionnaireResponse"],
        "resourceType": "QuestionnaireResponse",
        "questionnaire": fhir_questionnaire.get("id"),
        "item": [],
    }
    env["resource"] = root
    env["questionnaire"] = env["Questionnaire"]
    for variable in get_variable(exts):
        env[variable["name"]] = await resolve_expression(
            client, {}, variable, env, f"variable.{variable['name']}"
        )

    for item in fhir_questionnaire["item"]:
        root["item"].extend(await _handle_item(client, item, env, {}))

    return root


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
            if is_repeating:
                answers = [{make_value_key(type_): normalize_answer_value(type_, d)} for d in data]
            else:
                answers = [{make_value_key(type_): normalize_answer_value(type_, data[0])}]
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
