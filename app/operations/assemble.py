import json

from aiohttp import web
from funcy.colls import project
from funcy.seqs import concat, distinct
from funcy.types import is_mapping

from app.sdk import sdk

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


async def assemble_questionnaire(questionnaire, root_elements):
    if is_mapping(questionnaire) and "item" in questionnaire:
        for item in questionnaire.item:
            if "subQuestionnaire" in item:
                sub = await sdk.client.resources("Questionnaire").get(
                    id=item.subQuestionnaire
                )
                propogate = project(dict(sub), PROPOGATE_ELEMENTS)
                root = project(dict(sub), WHITELISTED_ROOT_ELEMENTS.keys())
                for key, value in root.items():
                    uniqness = WHITELISTED_ROOT_ELEMENTS[key]
                    current = root_elements.get(key, [])
                    new = concat(current, value)
                    root_elements[key] = distinct(new, uniqness)
                sub = await assemble_questionnaire(sub, root_elements)
                dict.update(item, propogate)
                item.item = sub.item
                del item["subQuestionnaire"]
            if "item" in item:
                item.item = [
                    await assemble_questionnaire(i, root_elements) for i in item.item
                ]

    return questionnaire
