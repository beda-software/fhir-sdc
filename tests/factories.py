import json

from app.sdc.getters import (
    CHOICE_COLUMN_URL,
    CQF_LIBRARY_URL,
    INITIAL_EXPRESSION_URL,
    ITEM_POPULATION_CONTEXT_URL,
    LAUNCH_CONTEXT_URL,
    SOURCE_QUERIES_URL,
    VARIABLE_URL,
)

QUESTIONNAIRE_PROFILE_URL = (
    "https://emr-core.beda.software/StructureDefinition/fhir-emr-questionnaire"
)


def make_parameters(**payload):
    return {
        "resourceType": "Parameters",
        "parameter": [{"name": name, "resource": resource} for name, resource in payload.items()],
    }


def make_questionnaire(questionnaire):
    return {
        **questionnaire,
        "meta": {"profile": [QUESTIONNAIRE_PROFILE_URL]},
    }


async def create_questionnaire(fhir_client, questionnaire):
    q = fhir_client.resource(
        "Questionnaire",
        **make_questionnaire(questionnaire),
    )
    await q.save()
    assert q.id is not None
    return q


async def create_address_questionnaire(fhir_client):
    return await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_assemble_context_ext("prefix"),
            ],
            "item": [
                {
                    "linkId": "{{%prefix}}line-1",
                    "type": "string",
                    "extension": [make_initial_expression_ext("line[0]")],
                },
                {
                    "linkId": "{{%prefix}}line-2",
                    "type": "string",
                    "extension": [make_initial_expression_ext("line[1]")],
                    "enableWhen": [
                        {
                            "question": "{{%prefix}}line-1",
                            "operator": "exists",
                            "answer": {"boolean": True},
                        }
                    ],
                },
            ],
        },
    )


def make_launch_context_ext(name, type_):
    return {
        "url": LAUNCH_CONTEXT_URL,
        "extension": [
            {
                "url": "name",
                "valueCoding": {
                    "code": name,
                    "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                },
            },
            {"url": "type", "valueCode": type_},
        ],
    }


def make_source_queries_ext(reference):
    return {
        "url": SOURCE_QUERIES_URL,
        "valueReference": {"reference": reference},
    }


def make_item_population_context_ext(expression, name=None):
    return {
        "url": ITEM_POPULATION_CONTEXT_URL,
        "valueExpression": {
            "language": "text/fhirpath",
            "expression": expression,
            **({"name": name} if name else {}),
        },
    }


def make_initial_expression_ext(expression):
    return {
        "url": INITIAL_EXPRESSION_URL,
        "valueExpression": {"language": "text/fhirpath", "expression": expression},
    }


def make_choice_column_ext(path):
    return {
        "url": CHOICE_COLUMN_URL,
        "extension": [
            {"url": "forDisplay", "valueBoolean": True},
            {"url": "path", "valueString": path},
        ],
    }


def make_variable_ext(name, expression, language="text/fhirpath"):
    return {
        "url": VARIABLE_URL,
        "valueExpression": {
            "name": name,
            "language": language,
            "expression": expression,
        },
    }


def make_assemble_context_ext(context):
    return {
        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembleContext",
        "valueString": context,
    }


def make_sub_questionnaire_ext(questionnaire_id):
    return {
        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
        "valueCanonical": questionnaire_id,
    }


def make_assembled_from_ext(questionnaire_id):
    return {
        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembledFrom",
        "valueCanonical": questionnaire_id,
    }


def make_questionnaire_mapper_ext(mapping_id):
    return {
        "url": "https://emr-core.beda.software/StructureDefinition/questionnaire-mapper",
        "valueReference": {"reference": f"Mapping/{mapping_id}"},
    }


def make_questionnaire_embedded_mapper_ext(mapping_body: dict):
    language = "fpml" if mapping_body.get("type") == "FHIRPath" else "jute"
    return {
        "url": "https://emr-core.beda.software/StructureDefinition/questionnaire-mapper",
        "valueExpression": {
            "language": language,
            "expression": json.dumps(mapping_body),
        },
    }


def make_item_constraint_ext(*, key, requirements, severity, human, expression):
    return {
        "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-constraint",
        "extension": [
            {"url": "key", "valueId": key},
            {"url": "requirements", "valueString": requirements},
            {"url": "severity", "valueCode": severity},
            {"url": "human", "valueString": human},
            {"url": "expression", "valueString": expression},
        ],
    }


def make_target_structure_map_ext(structure_map_id):
    return {
        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap",
        "valueCanonical": structure_map_id,
    }


def make_cqf_library_ext(canonical):
    return {
        "url": CQF_LIBRARY_URL,
        "valueCanonical": canonical,
    }


def make_jute_structure_map(structure_map_id: str, template: dict) -> dict:
    """A StructureMap carrying a jute template where fhir-sdc looks for it."""
    return {
        "resourceType": "StructureMap",
        "id": structure_map_id,
        "url": f"http://example.com/StructureMap/{structure_map_id}",
        "name": structure_map_id,
        "status": "active",
        "group": [
            {
                "name": "jute-group",
                "typeMode": "none",
                "input": [{"name": "source", "mode": "source"}],
                "rule": [
                    {
                        "name": "apply-jute",
                        "source": [{"context": "source"}],
                        "extension": [
                            {
                                "url": "http://beda.software/fhir-extensions/jute-body",
                                "valueString": json.dumps(template),
                            }
                        ],
                    }
                ],
            }
        ],
    }


JUTE_BODY_EXTENSION_SD = {
    "resourceType": "StructureDefinition",
    "id": "jute-body",
    "url": "http://beda.software/fhir-extensions/jute-body",
    "name": "JuteBody",
    "status": "active",
    "kind": "complex-type",
    "abstract": False,
    "type": "Extension",
    "context": [{"type": "element", "expression": "Element"}],
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
    "derivation": "constraint",
    "differential": {
        "element": [
            {"id": "Extension", "path": "Extension", "max": "1"},
            {
                "id": "Extension.url",
                "path": "Extension.url",
                "fixedUri": "http://beda.software/fhir-extensions/jute-body",
            },
            {
                "id": "Extension.value[x]",
                "path": "Extension.value[x]",
                "type": [{"code": "string"}],
            },
        ]
    },
}
