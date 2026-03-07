from fhirpy.base.exceptions import OperationOutcome
from funcy import is_list

from .getters import get_initial_expression, get_item_context, get_item_population_context, get_launch_context
from .utils import get_type, load_source_queries, make_value_key, validate_context
from app.cached_fhirpath import fhirpath


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
        "resourceType": "QuestionnaireResponse",
        "questionnaire": fhir_questionnaire.get("id"),
        "item": [],
    }
    env["resource"] = root
    env["questionnaire"] = env["Questionnaire"]

    for item in fhir_questionnaire["item"]:
        root["item"].extend(_handle_item(item, env, {}))

    return root


def _handle_item(item, env, context):
    env["qitem"] = item

    def init_item():
        new_item = {"linkId": item["linkId"]}
        if "text" in item:
            new_item["text"] = item["text"]
        return new_item


    item_exts = item.get("extension", [])

    item_context = get_item_context(item_exts)
    if item_context:
        context = fhirpath(context, item_context["expression"], env)

    item_population_context = get_item_population_context(item_exts)
    if item_population_context:
        context = fhirpath(context, item_population_context["expression"], env)

    if (
        item["type"] == "group"
        and item.get("repeats", False) is True
        and is_list(context)
    ):
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

    initial_expression = get_initial_expression(item_exts)
    if context and initial_expression and item.get("repeats", False) is True:
        answers = []
        for item_context in context:
            data = fhirpath(
                item_context,
                initial_expression["expression"],
                env,
            )
            if data and len(data):
                type_ = get_type(item, data)
                answers.extend([{make_value_key(type_): d} for d in data])
        if answers:
            root_item["answer"] = answers
    elif initial_expression:
        answers = []
        try:
            data = fhirpath(context, initial_expression["expression"], env)
        except Exception as e:
            raise OperationOutcome(
                f'Error: "{initial_expression["expression"]}" - {str(e)}'
            )
        if data and len(data):
            type_ = get_type(item, data)
            if item.get("repeats") is True:
                answers = [{make_value_key(type_): d} for d in data]
            else:
                answers = [{make_value_key(type_): data[0]}]
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
