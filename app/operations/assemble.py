import asyncio
import json

from aiohttp import web
from funcy.colls import project
from funcy.seqs import concat, distinct, flatten

from app.sdk import sdk

from .utils import prepare_bundle, prepare_varaibles

WHITELISTED_ROOT_ELEMENTS = {
    "launchContext": lambda i: i["name"],
    "contained": lambda i: i["id"],
    "sourceQueries": lambda i: i.get("id", i["localRef"]),
    "cqf-library": lambda i: i["expression"],
}

PROPOGATE_ELEMENTS = ["itemContext"]


@sdk.operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
async def assemble(operation, request):
    questionnaire = await sdk.client.resources("Questionnaire").get(
        id=request["route-params"]["id"]
    )
    root_elements = project(dict(questionnaire), WHITELISTED_ROOT_ELEMENTS.keys())
    await assemble_questionnaire(questionnaire, root_elements)
    dict.update(questionnaire, root_elements)
    questionnaire.assembledFrom = questionnaire["id"]
    del questionnaire["id"]
    return web.json_response(questionnaire, dumps=lambda a: json.dumps(a, default=list))


async def load_sub_questionanire(root_elements, parent_item, item):
    if "subQuestionnaire" in item:
        sub = await sdk.client.resources("Questionnaire").get(id=item.subQuestionnaire)

        varaibles = prepare_varaibles(item)

        sub = prepare_bundle(sub, varaibles)

        propogate = project(dict(sub), PROPOGATE_ELEMENTS)
        dict.update(parent_item, propogate)

        root = project(dict(sub), WHITELISTED_ROOT_ELEMENTS.keys())
        for key, value in root.items():
            uniqness = WHITELISTED_ROOT_ELEMENTS[key]
            current = root_elements.get(key, [])
            new = concat(current, value)
            root_elements[key] = distinct(new, uniqness)

        return sub["item"]

    return item


async def assemble_questionnaire(questionnaire_item, root_elements):
    if "item" in questionnaire_item:
        with_sub_items_futures = (
            load_sub_questionanire(root_elements, questionnaire_item, i)
            for i in questionnaire_item["item"]
        )
        with_sub_items = await asyncio.gather(*with_sub_items_futures)
        assembled_futures = (
            assemble_questionnaire(i, root_elements) for i in flatten(with_sub_items)
        )
        assembled = await asyncio.gather(*assembled_futures)
        questionnaire_item["item"] = assembled
    return questionnaire_item
