QUESTIONNAIRE_PROFILE_URL = (
    "https://emr-core.beda.software/StructureDefinition/fhir-emr-questionnaire"
)


def make_parameters(**payload):
    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": name, "resource": resource} for name, resource in payload.items()
        ],
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
        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
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
        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
        "valueReference": {"reference": reference},
    }


def make_item_population_context_ext(expression):
    return {
        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
        "valueExpression": {"language": "text/fhirpath", "expression": expression},
    }


def make_initial_expression_ext(expression):
    return {
        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
        "valueExpression": {"language": "text/fhirpath", "expression": expression},
    }


def make_variable_ext(name, expression):
    return {
        "url": "http://hl7.org/fhir/StructureDefinition/variable",
        "valueExpression": {
            "name": name,
            "language": "text/fhirpath",
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
