meta_resources = {
    "Attribute": {
        "Questionnaire.sourceQueries": {
            "type": {"resourceType": "Entity", "id": "Reference"},
            "path": ["sourceQueries"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
            "isCollection": True,
        },
        "Questionnaire.launchContext": {
            # 'type': {'resourceType': 'Entity',  'id': 'string'},
            "path": ["launchContext"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "isCollection": True,
        },
        "Questionnaire.launchContext.name": {
            "type": {"resourceType": "Entity", "id": "id"},
            "path": ["launchContext", "name"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "name",
        },
        "Questionnaire.launchContext.type": {
            "type": {"resourceType": "Entity", "id": "code"},
            "path": ["launchContext", "type"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "type",
        },
        "Questionnaire.launchContext.description": {
            "type": {"resourceType": "Entity", "id": "string"},
            "path": ["launchContext", "description"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "description",
        },
        "Questionnaire.item.initialExpression": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "initialExpression"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
        },
        "Questionnaire.item.itemContext": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "itemContext"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemContext",
        },
        "Questionnaire.item.hidden": {
            "type": {"resourceType": "Entity", "id": "boolean"},
            "path": ["item", "hidden"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
        },
        "Questionnaire.mapping": {
            "type": {"resourceType": "Entity", "id": "Reference"},
            "path": ["mapping"],
            "refers": ["Mapping"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "isCollection": True,
        },
    },
}
