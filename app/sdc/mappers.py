import json

from .getters import QUESTIONNAIRE_MAPPER_URL, TARGET_STRUCTURE_MAP_URL

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
        url = extension["url"]
        expression = extension.get("valueExpression", {}).get("expression")
        if url == TARGET_STRUCTURE_MAP_URL:
            canonical = extension["valueCanonical"]
            mappers.append(await resolve_structure_map_template(user_client, canonical))
        elif url == QUESTIONNAIRE_MAPPER_URL and "valueReference" in extension:
            mappers.append(await resolve_mapping(user_client, extension["valueReference"]))
        elif url == QUESTIONNAIRE_MAPPER_URL and expression:
            mappers.append(json.loads(expression))
    return mappers


async def resolve_structure_map_template(user_client, canonical):
    structure_map_id = canonical.split("/")[-1]
    structure_map = await user_client.resources("StructureMap").search(_id=structure_map_id).get()
    return json.loads(structure_map.get_by_path(JUTE_BODY_PATH))


async def resolve_mapping(user_client, reference):
    mapping_id = reference["reference"].split("/")[-1]
    return await user_client.resources("Mapping").search(_id=mapping_id).get()
