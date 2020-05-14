import logging

from aiohttp import web
from fhirpy.base.utils import AttrDict
from funcy.types import is_list, is_mapping

from app.sdk import sdk


@sdk.operation(["GET"], ["Questionnaire", {"name": "id"}, "$assemble"])
async def assemble(operation, request):
    questionnaire = await sdk.client.resources("Questionnaire").get(
        id=request["route-params"]["id"]
    )
    await assemble_questionnaire(questionnaire)
    return web.json_response(questionnaire)


async def assemble_questionnaire(questionnaire):
    if is_mapping(questionnaire) and "item" in questionnaire:
        for item in questionnaire.item:
            if "subQuestionnaire" in item:
                sub = await sdk.client.resources("Questionnaire").get(
                    id=item.subQuestionnaire
                )
                sub = await assemble_questionnaire(sub)
                item.item = sub.item
                del item["subQuestionnaire"]
            if "item" in item:
                item.item = [await assemble_questionnaire(i) for i in item.item]

    return questionnaire
