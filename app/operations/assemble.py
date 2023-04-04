import asyncio
import json

from aiohttp import web
from funcy.colls import project
from funcy.seqs import concat, distinct, flatten

from app.sdk import sdk

from .utils import get_user_sdk_client, prepare_link_ids, prepare_variables, validate_context

WHITELISTED_ROOT_ELEMENTS = {
    "launchContext": lambda i: i["name"],
    "mapping": lambda i: i["id"],
    "contained": lambda i: i["id"],
    "sourceQueries": lambda i: i.get("id", i["localRef"]),
    "cqf-library": lambda i: i["expression"],
}

PROPAGATE_ELEMENTS = ["itemContext", "itemPopulationContext"]


@sdk.operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
async def assemble(_operation, request):
    client = get_user_sdk_client(request)
    questionnaire = await client.resources("Questionnaire").get(id=request["route-params"]["id"])
    root_elements = project(dict(questionnaire), WHITELISTED_ROOT_ELEMENTS.keys())
    questionnaire["item"] = await assemble_questionnaire(
        client, questionnaire, questionnaire["item"], root_elements
    )
    dict.update(questionnaire, root_elements)
    questionnaire.assembledFrom = questionnaire["id"]
    del questionnaire["id"]
    return web.json_response(questionnaire, dumps=lambda a: json.dumps(a, default=list))


async def load_sub_questionnaire(client, root_elements, parent_item, item):
    if "subQuestionnaire" in item:
        sub = await client.resources("Questionnaire").get(id=item["subQuestionnaire"])

        variables = prepare_variables(item)
        if validate_assemble_context(sub, variables):
            sub = prepare_link_ids(sub, variables)

        propagate = project(dict(sub), PROPAGATE_ELEMENTS)
        dict.update(parent_item, propagate)

        root = project(dict(sub), WHITELISTED_ROOT_ELEMENTS.keys())
        for key, value in root.items():
            uniqueness = WHITELISTED_ROOT_ELEMENTS[key]
            current = root_elements.get(key, [])
            new = concat(current, value)
            root_elements[key] = distinct(new, uniqueness)
        return sub["item"]

    return item


async def assemble_questionnaire(client, parent, questionnaire_items, root_elements):
    with_sub_items = questionnaire_items
    while len([i for i in with_sub_items if "subQuestionnaire" in i]):
        with_sub_items_futures = (
            load_sub_questionnaire(client, root_elements, parent, i) for i in with_sub_items
        )
        with_sub_items = list(flatten(await asyncio.gather(*with_sub_items_futures)))

    resp = []
    for i in with_sub_items:
        if "item" in i:
            i["item"] = await assemble_questionnaire(client, i, i["item"], root_elements)
        resp.append(i)
    return resp


def validate_assemble_context(questionnaire, variables: dict):
    if "assembleContext" not in questionnaire:
        return False

    validate_context(questionnaire["assembleContext"], variables)

    return True
