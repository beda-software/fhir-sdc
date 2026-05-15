from funcy.seqs import flatten

from .getters import (
    ASSEMBLED_FROM_URL,
    CQF_LIBRARY_URL,
    ITEM_CONTEXT_URL,
    ITEM_POPULATION_CONTEXT_URL,
    LAUNCH_CONTEXT_URL,
    QUESTIONNAIRE_MAPPER_URL,
    SOURCE_QUERIES_URL,
    TARGET_STRUCTURE_MAP_URL,
    get_assemble_context,
    get_sub_questionnaire,
)
from .utils import (
    prepare_assemble_variables,
    prepare_link_ids,
    validate_assemble_context,
)


def _launch_context_key(ext):
    name_ext = next(
        (e for e in ext.get("extension", []) if e.get("url") == "name"), None
    )
    if name_ext:
        coding = name_ext.get("valueCoding", {})
        return coding.get("code")
    return None


WHITELISTED_EXTENSION_URLS = {
    LAUNCH_CONTEXT_URL: _launch_context_key,
    QUESTIONNAIRE_MAPPER_URL: lambda ext: ext.get("valueReference", {}).get("reference", "").split("/")[-1],
    SOURCE_QUERIES_URL: lambda ext: ext.get("valueReference", {}).get("reference", "").removeprefix("#"),
    TARGET_STRUCTURE_MAP_URL: lambda ext: ext.get("valueCanonical"),
    CQF_LIBRARY_URL: lambda ext: ext.get("valueCanonical"),
}

PROPAGATE_EXTENSION_URLS = {ITEM_CONTEXT_URL, ITEM_POPULATION_CONTEXT_URL}


def _merge_sub_ext(accumulated: list, ext: dict):
    """Append a unique whitelisted sub-questionnaire extension to accumulated list."""
    url = ext.get("url")
    if url not in WHITELISTED_EXTENSION_URLS:
        return
    key_fn = WHITELISTED_EXTENSION_URLS[url]
    key = key_fn(ext)
    if not any(e.get("url") == url and key_fn(e) == key for e in accumulated):
        accumulated.append(ext)


def _merge_root_ext(accumulated: list, ext: dict):
    """Merge a root questionnaire whitelisted extension into accumulated list.

    Root extensions are inserted *before* the first same-URL extension already
    present (so root entries lead within their URL group), or appended when the
    URL is not yet in the list.
    """
    url = ext.get("url")
    if url not in WHITELISTED_EXTENSION_URLS:
        return
    key_fn = WHITELISTED_EXTENSION_URLS[url]
    key = key_fn(ext)
    if any(e.get("url") == url and key_fn(e) == key for e in accumulated):
        return
    first_same_url_idx = next(
        (i for i, e in enumerate(accumulated) if e.get("url") == url), -1
    )
    if first_same_url_idx >= 0:
        accumulated.insert(first_same_url_idx, ext)
    else:
        accumulated.append(ext)


async def assemble(client, questionnaire):
    original_exts = list(questionnaire.get("extension", []))
    non_whitelisted_root_exts = [
        e for e in original_exts if e.get("url") not in WHITELISTED_EXTENSION_URLS
    ]
    root_whitelisted_exts = [
        e for e in original_exts if e.get("url") in WHITELISTED_EXTENSION_URLS
    ]
    root_contained = list(questionnaire.get("contained", []))
    sub_exts = []  # whitelisted extensions collected from sub-questionnaires

    sub_questionnaire_ids_map = await _load_sub_questionnaires(
        client, questionnaire.get("item", [])
    )

    questionnaire["item"] = _assemble_questionnaire(
        questionnaire,
        questionnaire.get("item", []),
        sub_exts,
        root_contained,
        sub_questionnaire_ids_map,
    )

    for ext in root_whitelisted_exts:
        _merge_root_ext(sub_exts, ext)

    sub_exts.append({"url": ASSEMBLED_FROM_URL, "valueCanonical": questionnaire["id"]})
    questionnaire["extension"] = non_whitelisted_root_exts + sub_exts
    if root_contained:
        questionnaire["contained"] = root_contained
    del questionnaire["id"]
    return questionnaire


def _collect_sub_questionnaire_ids_map(questionnaire_items, sub_questionnaire_ids_map: dict):
    result_map = sub_questionnaire_ids_map.copy()
    for item in questionnaire_items:
        sub_q = get_sub_questionnaire(item.get("extension", []))
        if sub_q and sub_q not in result_map:
            result_map[sub_q] = None
        else:
            result_map = _collect_sub_questionnaire_ids_map(item.get("item", []), result_map)
    return result_map


async def _load_sub_questionnaires(
    client,
    questionnaire_items,
    prev_sub_questionnaire_ids_map: dict = {},
):
    sub_questionnaire_ids_map = _collect_sub_questionnaire_ids_map(
        questionnaire_items, prev_sub_questionnaire_ids_map
    )

    not_loaded = [k for k, v in sub_questionnaire_ids_map.items() if v is None]
    if not not_loaded:
        return sub_questionnaire_ids_map

    id_query = ",".join(not_loaded)
    subqs = await client.resources("Questionnaire").search(_id=id_query).fetch_all()
    fhir_subqs = [dict(sq) for sq in subqs]

    subqs_all_items = []
    for fhir_subq in fhir_subqs:
        if (
            fhir_subq["id"] in sub_questionnaire_ids_map
            and sub_questionnaire_ids_map[fhir_subq["id"]] is None
        ):
            sub_questionnaire_ids_map[fhir_subq["id"]] = fhir_subq
        if fhir_subq.get("item"):
            subqs_all_items.extend(fhir_subq["item"])

    sub_questionnaire_ids_map = await _load_sub_questionnaires(
        client, subqs_all_items, sub_questionnaire_ids_map
    )
    return sub_questionnaire_ids_map


def _load_sub_questionnaire(sub_exts, root_contained, parent_item, item, sub_questionnaire_ids_map):
    sub_q_id = get_sub_questionnaire(item.get("extension", []))
    if sub_q_id:
        fhir_subq = sub_questionnaire_ids_map[sub_q_id]

        variables = prepare_assemble_variables(item)
        if _validate_assemble_context(fhir_subq, variables):
            fhir_subq = prepare_link_ids(fhir_subq, variables)

        _propagate_extensions(parent_item, fhir_subq)

        for ext in fhir_subq.get("extension", []):
            _merge_sub_ext(sub_exts, ext)

        for contained_item in fhir_subq.get("contained", []):
            if not any(c["id"] == contained_item["id"] for c in root_contained):
                root_contained.append(contained_item)

        return fhir_subq.get("item", [])

    return item


def _propagate_extensions(parent_item, sub_questionnaire):
    parent_exts = list(parent_item.get("extension", []))
    for ext in sub_questionnaire.get("extension", []):
        if ext.get("url") in PROPAGATE_EXTENSION_URLS:
            if not any(e.get("url") == ext["url"] for e in parent_exts):
                parent_exts.append(ext)
    if parent_exts:
        parent_item["extension"] = parent_exts


def _assemble_questionnaire(
    parent,
    questionnaire_items,
    sub_exts,
    root_contained,
    sub_questionnaire_ids_map,
):
    with_sub_items = questionnaire_items
    while any(get_sub_questionnaire(i.get("extension", [])) for i in with_sub_items):
        with_sub_items = list(flatten(
            _load_sub_questionnaire(sub_exts, root_contained, parent, i, sub_questionnaire_ids_map)
            for i in with_sub_items
        ))

    resp = []
    for i in with_sub_items:
        if "item" in i:
            i["item"] = _assemble_questionnaire(
                i,
                i["item"],
                sub_exts,
                root_contained,
                sub_questionnaire_ids_map,
            )
        resp.append(i)
    return resp


def _validate_assemble_context(questionnaire, variables: dict):
    assemble_ctx = get_assemble_context(questionnaire.get("extension", []))
    if not assemble_ctx:
        return False
    validate_assemble_context(assemble_ctx, variables)
    return True
