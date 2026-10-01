import json

from fhirpy.base.exceptions import OperationOutcome

from .getters import QUESTIONNAIRE_MAPPER_URL, TARGET_STRUCTURE_MAP_URL
from .utils import resolve_by_canonical

JUTE_BODY_PATH = [
    "group",
    {"name": "jute-group"},
    "rule",
    {"name": "apply-jute"},
    "extension",
    {"url": "http://beda.software/fhir-extensions/jute-body"},
    "valueString",
]


async def load_mappers(user_client, questionnaire) -> list:
    """Every mapper the Questionnaire names, in extension order."""
    mappers = []
    for extension in questionnaire.get("extension", []):
        url = extension.get("url")
        canonical = extension.get("valueCanonical")
        reference = (extension.get("valueReference") or {}).get("reference")
        expression = (extension.get("valueExpression") or {}).get("expression")
        if url == TARGET_STRUCTURE_MAP_URL and canonical:
            mappers.append(await resolve_structure_map_template(user_client, canonical))
        elif url == QUESTIONNAIRE_MAPPER_URL and reference:
            mappers.append(await resolve_mapping(user_client, reference))
        elif url == QUESTIONNAIRE_MAPPER_URL and expression:
            mappers.append(json.loads(expression))
    return mappers


async def resolve_structure_map_template(user_client, canonical):
    structure_map = await resolve_by_canonical(user_client, "StructureMap", canonical)
    template = structure_map.get_by_path(JUTE_BODY_PATH)
    if not template:
        raise OperationOutcome(f"StructureMap `{canonical}` carries no jute body")

    return json.loads(template)


async def resolve_mapping(user_client, reference):
    mapping_id = reference.split("/")[-1]
    return await user_client.resources("Mapping").search(_id=mapping_id).get()
