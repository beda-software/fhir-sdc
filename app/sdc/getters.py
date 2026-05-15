from .typings import Expression, LaunchContext, Reference


INITIAL_EXPRESSION_URL = (
    "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression"
)
ITEM_CONTEXT_URL = (
    "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemContext"
)
ITEM_POPULATION_CONTEXT_URL = "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext"
LAUNCH_CONTEXT_URL = (
    "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext"
)
SOURCE_QUERIES_URL = (
    "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries"
)
VARIABLE_URL = "http://hl7.org/fhir/StructureDefinition/variable"
SUB_QUESTIONNAIRE_URL = (
    "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire"
)
ASSEMBLE_CONTEXT_URL = (
    "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembleContext"
)
QUESTIONNAIRE_MAPPER_URL = (
    "https://emr-core.beda.software/StructureDefinition/questionnaire-mapper"
)
TARGET_STRUCTURE_MAP_URL = (
    "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap"
)
CQF_LIBRARY_URL = "http://hl7.org/fhir/StructureDefinition/cqf-library"
ITEM_CONSTRAINT_URL = "http://hl7.org/fhir/StructureDefinition/questionnaire-constraint"
ASSEMBLED_FROM_URL = (
    "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembledFrom"
)


def _find_extension(extensions: list, url: str):
    """Return the first extension with the given url, or None."""
    exts = _find_extensions(extensions, url)
    return exts[0] if exts else None


def _find_extensions(extensions: list, url: str) -> list:
    """Return all extensions with the given url."""
    if not extensions:
        return []
    return [ext for ext in extensions if ext.get("url") == url]


def get_initial_expression(extensions: list) -> Expression | None:
    ext = _find_extension(extensions, INITIAL_EXPRESSION_URL)
    return ext.get("valueExpression") if ext else None


def get_item_context(extensions: list) -> Expression | None:
    ext = _find_extension(extensions, ITEM_CONTEXT_URL)
    return ext.get("valueExpression") if ext else None


def get_item_population_context(extensions: list) -> Expression | None:
    ext = _find_extension(extensions, ITEM_POPULATION_CONTEXT_URL)
    return ext.get("valueExpression") if ext else None


def get_variable(extensions: list) -> list[Expression]:
    exts = _find_extensions(extensions, VARIABLE_URL)
    return [ext.get("valueExpression") for ext in exts]


def get_launch_context(extensions: list) -> list[LaunchContext]:
    res = []
    for ext in _find_extensions(extensions, LAUNCH_CONTEXT_URL):
        name_ext = _find_extension(ext["extension"], "name")
        if not name_ext:
            continue
        type_exts = _find_extensions(ext["extension"], "type")
        if not type_exts:
            continue
        types = [ext.get("valueCode") for ext in type_exts]
        types = [t for t in types if t]
        if not types:
            continue
        res.append(
            LaunchContext(
                name=name_ext.get("valueCoding"),
                type=types,
            )
        )
    return res


def get_source_queries(extensions: list) -> list[Reference]:
    exts = _find_extensions(extensions, SOURCE_QUERIES_URL)
    return [ext["valueReference"] for ext in exts if ext.get("valueReference")]


def get_sub_questionnaire(extensions: list) -> str | None:
    ext = _find_extension(extensions, SUB_QUESTIONNAIRE_URL)
    return ext.get("valueCanonical") if ext else None


def get_assemble_context(extensions: list) -> list[str]:
    exts = _find_extensions(extensions, ASSEMBLE_CONTEXT_URL)
    return [ext["valueString"] for ext in exts if ext.get("valueString")]


def get_questionnaire_mapper(extensions: list) -> list[Reference]:
    exts = _find_extensions(extensions, QUESTIONNAIRE_MAPPER_URL)
    return [ext["valueReference"] for ext in exts if ext.get("valueReference")]


def get_target_structure_map(extensions: list) -> list[str]:
    exts = _find_extensions(extensions, TARGET_STRUCTURE_MAP_URL)
    return [ext["valueCanonical"] for ext in exts if ext.get("valueCanonical")]


def get_cqf_library(extensions: list) -> list[str]:
    exts = _find_extensions(extensions, CQF_LIBRARY_URL)
    return [ext["valueCanonical"] for ext in exts if ext.get("valueCanonical")]


def get_item_constraints(extensions: list) -> list[dict]:
    """Return list of dicts with 'expression' and other constraint fields."""
    result = []
    for ext in _find_extensions(extensions, ITEM_CONSTRAINT_URL):
        sub = {e["url"]: e for e in ext.get("extension", [])}
        expression = sub.get("expression", {}).get("valueString")
        if expression:
            result.append({
                "key": sub.get("key", {}).get("valueId"),
                "severity": sub.get("severity", {}).get("valueCode"),
                "human": sub.get("human", {}).get("valueString"),
                "expression": expression,
            })
    return result
