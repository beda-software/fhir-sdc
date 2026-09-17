"""Only user-entered answers are faked; $populate, constraints and the Mapping run for real."""

from collections.abc import Mapping, Sequence
from typing import Any, NamedTuple, cast

import fhirpy_types_r4b as r4b
from fhirpy import AsyncFHIRClient

from fhir_sdc_testkit.extraction import raise_for_extraction_errors
from fhir_sdc_testkit.sugar import Answers


class ItemPath(NamedTuple):
    path: tuple[str, ...]
    item: r4b.QuestionnaireItem


async def populate_and_extract(
    fhir_client: AsyncFHIRClient,
    questionnaire_id: str,
    *,
    parameters: r4b.Parameters | None = None,
    answers: Answers,
) -> r4b.QuestionnaireResponse:
    """Returns the saved QuestionnaireResponse the extraction ran on. A failed constraint raises."""
    given = list(parameters.parameter or []) if parameters else []
    questionnaire = await fhir_client.get(r4b.Questionnaire, questionnaire_id)
    populated = await fhir_client.execute(
        f"Questionnaire/{questionnaire_id}/$populate",
        data=r4b.Parameters(parameter=given).model_dump(),
    )
    response = fill_questionnaire_response(questionnaire, read_populated(populated), answers)
    saved = await fhir_client.create(response)
    extract_parameters = [
        r4b.ParametersParameter(name="questionnaire", resource=questionnaire),
        # fhir-sdc reads the response from `questionnaire_response`; SDC names it with a hyphen.
        r4b.ParametersParameter(name="questionnaire_response", resource=saved),
        r4b.ParametersParameter(name="questionnaire-response", resource=saved),
        *given,
    ]
    extracted = await fhir_client.execute(
        "Questionnaire/$extract", data=r4b.Parameters(parameter=extract_parameters).model_dump()
    )
    raise_for_extraction_errors(extracted)
    return saved


def read_populated(populated: Mapping[str, Any]) -> r4b.QuestionnaireResponse:
    """$populate answers with Parameters, not a bare response, once a `context` is passed."""
    if populated.get("resourceType") == "Parameters":
        populated = next(p for p in populated["parameter"] if p["name"] == "response")["resource"]
    return r4b.QuestionnaireResponse.model_validate(populated)


def fill_questionnaire_response(
    questionnaire: r4b.Questionnaire, populated: r4b.QuestionnaireResponse, answers: Answers
) -> r4b.QuestionnaireResponse:
    """Set each answer at its linkId's nesting in the Questionnaire, replacing a populated one."""
    response = populated.model_copy(deep=True, update={"status": "completed"})
    if response.item is None:
        response.item = []
    fill_items(
        questionnaire.item or [], response.item, answers, scope=f"Questionnaire/{questionnaire.id}"
    )
    sort_items(questionnaire.item or [], response.item)
    return response


def sort_items(
    items: list[r4b.QuestionnaireItem], children: list[r4b.QuestionnaireResponseItem]
) -> None:
    """Answered items are appended as they come; a response follows the Questionnaire's order."""
    order = {item.linkId: index for index, item in enumerate(items)}
    children.sort(key=lambda child: order.get(child.linkId, len(order)))
    definitions = {item.linkId: item for item in items}
    for child in children:
        definition = definitions.get(child.linkId)
        if definition is not None and child.item:
            sort_items(definition.item or [], child.item)


def fill_items(
    items: list[r4b.QuestionnaireItem],
    children: list[r4b.QuestionnaireResponseItem],
    answers: Answers,
    *,
    scope: str,
) -> None:
    paths = build_link_id_paths(items)
    for link_id, value in answers.items():
        if link_id not in paths:
            raise KeyError(f"{link_id!r} is not an item of {scope} outside a repeating group")

        path, item = paths[link_id]
        siblings = find_or_create_siblings(children, path)
        if is_repeating_group(item):
            fill_occurrences(item, siblings, cast(Sequence[Answers], value))
        else:
            find_or_append_item(siblings, link_id).answer = list(
                cast(Sequence[r4b.QuestionnaireResponseItemAnswer], value)
            )


def build_link_id_paths(
    items: list[r4b.QuestionnaireItem], ancestors: tuple[str, ...] = ()
) -> dict[str, ItemPath]:
    """linkId → the linkIds from the top-level item down to it. Repeating items are not descended."""
    paths: dict[str, ItemPath] = {}
    for item in items:
        path = (*ancestors, item.linkId)
        paths[item.linkId] = ItemPath(path, item)
        if not item.repeats:
            paths.update(build_link_id_paths(item.item or [], path))
    return paths


def is_repeating_group(item: r4b.QuestionnaireItem) -> bool:
    return item.type == "group" and bool(item.repeats)


def find_or_create_siblings(
    children: list[r4b.QuestionnaireResponseItem], path: tuple[str, ...]
) -> list[r4b.QuestionnaireResponseItem]:
    """The item list holding the path's last linkId, creating the groups above it."""
    for link_id in path[:-1]:
        parent = find_or_append_item(children, link_id)
        if parent.item is None:
            parent.item = []
        children = parent.item
    return children


def find_or_append_item(
    children: list[r4b.QuestionnaireResponseItem], link_id: str
) -> r4b.QuestionnaireResponseItem:
    for child in children:
        if child.linkId == link_id:
            return child

    item = r4b.QuestionnaireResponseItem(linkId=link_id)
    children.append(item)
    return item


def fill_occurrences(
    group: r4b.QuestionnaireItem,
    siblings: list[r4b.QuestionnaireResponseItem],
    answer_sets: Sequence[Answers],
) -> None:
    """One answer set per occurrence, positionally over the populated ones. Extra ones are kept."""
    occurrences = find_or_append_occurrences(siblings, group.linkId, len(answer_sets))
    for occurrence, answers in zip(occurrences, answer_sets, strict=True):
        if occurrence.item is None:
            occurrence.item = []
        fill_items(
            group.item or [], occurrence.item, answers, scope=f"repeating group {group.linkId!r}"
        )


def find_or_append_occurrences(
    children: list[r4b.QuestionnaireResponseItem], link_id: str, count: int
) -> list[r4b.QuestionnaireResponseItem]:
    occurrences = [child for child in children if child.linkId == link_id]
    while len(occurrences) < count:
        item = r4b.QuestionnaireResponseItem(linkId=link_id)
        children.append(item)
        occurrences.append(item)
    return occurrences[:count]
