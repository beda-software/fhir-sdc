import asyncio

from funcy.colls import project
from funcy.seqs import concat, distinct, flatten

from .utils import prepare_link_ids, prepare_variables, validate_context

WHITELISTED_ROOT_ELEMENTS = {
    "launchContext": lambda i: i["name"]["code"],
    "mapping": lambda i: i["id"],
    "contained": lambda i: i["id"],
    "sourceQueries": lambda i: i.get("id", i["localRef"]),
    "cqf-library": lambda i: i["expression"],
    "targetStructureMap": lambda i: i,
}

PROPAGATE_ELEMENTS = ["itemContext", "itemPopulationContext"]


async def assemble(client, fce_questionnaire, to_first_class_extension_async):
    root_elements = project(dict(fce_questionnaire), WHITELISTED_ROOT_ELEMENTS.keys())
    fce_questionnaire["item"] = await _assemble_questionnaire(
        client,
        fce_questionnaire,
        fce_questionnaire["item"],
        root_elements,
        to_first_class_extension_async,
    )
    dict.update(fce_questionnaire, root_elements)
    fce_questionnaire["assembledFrom"] = fce_questionnaire["id"]
    del fce_questionnaire["id"]
    return fce_questionnaire


async def _load_sub_questionnaire(
    client, root_elements, parent_item, item, to_first_class_extension_async
):
    if "subQuestionnaire" in item:
        fhir_subq = (
            await client.resources("Questionnaire").search(_id=item["subQuestionnaire"]).get()
        )
        fce_subq = await to_first_class_extension_async(fhir_subq)

        variables = prepare_variables(item)
        if _validate_assemble_context(fce_subq, variables):
            fce_subq = prepare_link_ids(fce_subq, variables)

        propagate = project(dict(fce_subq), PROPAGATE_ELEMENTS)
        dict.update(parent_item, propagate)

        root = project(dict(fce_subq), WHITELISTED_ROOT_ELEMENTS.keys())
        for key, value in root.items():
            uniqueness = WHITELISTED_ROOT_ELEMENTS[key]
            current = root_elements.get(key, [])
            new = concat(current, value)
            root_elements[key] = distinct(new, uniqueness)
        return fce_subq["item"]

    return item


async def _assemble_questionnaire(
    client, parent, questionnaire_items, root_elements, to_first_class_extension_async
):
    with_sub_items = questionnaire_items
    while len([i for i in with_sub_items if "subQuestionnaire" in i]) > 0:
        with_sub_items_futures = (
            _load_sub_questionnaire(
                client, root_elements, parent, i, to_first_class_extension_async
            )
            for i in with_sub_items
        )
        with_sub_items = list(flatten(await asyncio.gather(*with_sub_items_futures)))

    resp = []
    for i in with_sub_items:
        if "item" in i:
            i["item"] = await _assemble_questionnaire(
                client, i, i["item"], root_elements, to_first_class_extension_async
            )
        resp.append(i)
    return resp


def _validate_assemble_context(questionnaire, variables: dict):
    if "assembleContext" not in questionnaire:
        return False

    validate_context(questionnaire["assembleContext"], variables)

    return True
