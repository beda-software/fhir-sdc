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

    sub_questionnaire_ids_map = await _load_sub_questionnaires(
        client, fce_questionnaire["item"], to_first_class_extension_async
    )

    fce_questionnaire["item"] = await _assemble_questionnaire(
        client,
        fce_questionnaire,
        fce_questionnaire["item"],
        root_elements,
        to_first_class_extension_async,
        sub_questionnaire_ids_map,
    )
    dict.update(fce_questionnaire, root_elements)
    fce_questionnaire["assembledFrom"] = fce_questionnaire["id"]
    del fce_questionnaire["id"]
    return fce_questionnaire


async def _collect_sub_questionnaire_ids_map(questionnaire_items, sub_questionnaire_ids_map: dict):
    result_map = {**sub_questionnaire_ids_map}

    for item in questionnaire_items:
        if "subQuestionnaire" in item and item["subQuestionnaire"] not in result_map:
            result_map[item["subQuestionnaire"]] = None
        else:
            result_map = await _collect_sub_questionnaire_ids_map(item.get("item", []), result_map)

    return result_map


async def _load_sub_questionnaires(
    client,
    questionnaire_items,
    to_first_class_extension_async,
    prev_sub_questionnaire_ids_map: dict = {},
):
    sub_questionnaire_ids_map = await _collect_sub_questionnaire_ids_map(
        questionnaire_items, prev_sub_questionnaire_ids_map
    )

    not_loaded_sub_questionnaire_ids = [
        k for k, v in sub_questionnaire_ids_map.items() if v is None
    ]
    if not not_loaded_sub_questionnaire_ids:
        return sub_questionnaire_ids_map

    id_query = ",".join(not_loaded_sub_questionnaire_ids)

    subqs = await client.resources("Questionnaire").search(_id=id_query).fetch_all()

    fhir_subqs_bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": dict(s)} for s in subqs],
    }
    fce_bundle = await to_first_class_extension_async(fhir_subqs_bundle)
    fce_subqs = [s["resource"] for s in fce_bundle["entry"]]

    subqs_all_items = []
    for fce_subq in fce_subqs:
        if (
            fce_subq["id"] in sub_questionnaire_ids_map
            and sub_questionnaire_ids_map[fce_subq["id"]] is None
        ):
            sub_questionnaire_ids_map[fce_subq["id"]] = fce_subq

        if fce_subq.get("item"):
            subqs_all_items.extend(fce_subq["item"])

    sub_questionnaire_ids_map = await _load_sub_questionnaires(
        client,
        subqs_all_items,
        to_first_class_extension_async,
        sub_questionnaire_ids_map,
    )

    return sub_questionnaire_ids_map


async def _load_sub_questionnaire(root_elements, parent_item, item, sub_questionnaire_ids_map):
    if "subQuestionnaire" in item:
        fce_subq = sub_questionnaire_ids_map[item["subQuestionnaire"]]

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
    client,
    parent,
    questionnaire_items,
    root_elements,
    to_first_class_extension_async,
    sub_questionnaire_ids_map,
):
    with_sub_items = questionnaire_items
    while len([i for i in with_sub_items if "subQuestionnaire" in i]) > 0:
        with_sub_items_futures = (
            _load_sub_questionnaire(root_elements, parent, i, sub_questionnaire_ids_map)
            for i in with_sub_items
        )
        with_sub_items = list(flatten(await asyncio.gather(*with_sub_items_futures)))

    resp = []
    for i in with_sub_items:
        if "item" in i:
            i["item"] = await _assemble_questionnaire(
                client,
                i,
                i["item"],
                root_elements,
                to_first_class_extension_async,
                sub_questionnaire_ids_map,
            )
        resp.append(i)
    return resp


def _validate_assemble_context(questionnaire, variables: dict):
    if "assembleContext" not in questionnaire:
        return False

    validate_context(questionnaire["assembleContext"], variables)

    return True
