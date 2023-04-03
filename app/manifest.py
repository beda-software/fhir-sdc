meta_resources_v2_7_0 = {
    "Attribute": {
        "Questionnaire.runOnBehalfOfRoot": {
            "type": {"resourceType": "Entity", "id": "boolean"},
            "path": ["runOnBehalfOfRoot"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "urn:ext:run-on-behalf-root",
            "description": "If true - add backward compatible behaviour for populating and extracting from root (means without access restrictions)"
        },
        "Questionnaire.sourceQueries": {
            "type": {"resourceType": "Entity", "id": "Reference"},
            "path": ["sourceQueries"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
            "isCollection": True,
        },
        "Questionnaire.launchContext": {
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
            "description": "Initial value for a question answer as determined by an evaluated expression."
        },
        "Questionnaire.itemContext": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["itemContext"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemContext",
            "description": "Deprecated in favour itemPopulationContext"
        },
        "Questionnaire.item.itemControl": {
            "type": {"resourceType": "Entity", "id": "CodeableConcept"},
            "path": ["item", "itemControl"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
            "description": "The type of data entry control or structure that should be used to render the item."
        },
        "Questionnaire.itemPopulationContext": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["itemPopulationContext"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
            "description": "Specifies a query that identifies the resource (or set of resources for a repeating item) that should be used to populate this Questionnaire or Questionnaire.item on initial population."
        },
        "Questionnaire.item.itemContext": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "itemContext"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemContext",
            "description": "Deprecated in favour itemPopulationContext"
        },
        "Questionnaire.item.itemPopulationContext": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "itemPopulationContext"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
            "description": "Specifies a query that identifies the resource (or set of resources for a repeating item) that should be used to populate this Questionnaire or Questionnaire.item on initial population."
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
            "description": "List of mapping resources that must be executed on extract"
        },
        "Questionnaire.item.subQuestionnaire": {
            "type": {"resourceType": "Entity", "id": "canonical"},
            "path": ["item", "subQuestionnaire"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "https://jira.hl7.org/browse/FHIR-22356#subQuestionnaire",
        },
        "Questionnaire.assembledFrom": {
            "type": {"resourceType": "Entity", "id": "canonical"},
            "path": ["assembledFrom"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "https://jira.hl7.org/browse/FHIR-22356#assembledFrom",
        },
        "Questionnaire.assembleContext": {
            "path": ["assembleContext"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembleContext",
            "isCollection": True,
        },
        "Questionnaire.assembleContext.name": {
            "type": {"resourceType": "Entity", "id": "id"},
            "path": ["assembleContext", "name"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "name",
        },
        "Questionnaire.assembleContext.type": {
            "type": {"resourceType": "Entity", "id": "code"},
            "path": ["assembleContext", "type"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "type",
        },
        "Questionnaire.assembleContext.description": {
            "type": {"resourceType": "Entity", "id": "string"},
            "path": ["assembleContext", "description"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "description",
        },
        "Questionnaire.variable": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["variable"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/StructureDefinition/variable",
            "isCollection": True,
            "description": "Variable specifying a logic to generate a variable for use in subsequent logic. "
                           "The name of the variable will be added to FHIRPath's context when processing descendants "
                           "of the element that contains this extension."
        },
        "Questionnaire.item.variable": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "variable"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/StructureDefinition/variable",
            "isCollection": True,
            "description": "Variable specifying a logic to generate a variable for use in subsequent logic. "
                           "The name of the variable will be added to FHIRPath's context when processing descendants "
                           "of the element that contains this extension."
        },
        # TODO: add support for root constraint definition
        # "Questionnaire.constraint": constraint_extension,
        "Questionnaire.item.constraint": {
            "path": ["item", "constraint"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/StructureDefinition/questionnaire-constraint",
            "isCollection": True,
            "description": "An invariant that must be satisfied before responses to the questionnaire can be considered \"complete\"."
        },
        "Questionnaire.item.constraint.key": {
            "type": {"resourceType": "Entity", "id": "id"},
            "path": ["item", "constraint", "key"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "key",
            "isRequired": True,
        },
        "Questionnaire.item.constraint.requirements": {
            "type": {"resourceType": "Entity", "id": "string"},
            "path": ["item", "constraint", "requirements"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "requirements",
        },
        "Questionnaire.item.constraint.severity": {
            "type": {"resourceType": "Entity", "id": "code"},
            "path": ["item", "constraint", "severity"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "severity",
            "isRequired": True,
        },
        "Questionnaire.item.constraint.human": {
            "type": {"resourceType": "Entity", "id": "string"},
            "path": ["item", "constraint", "human"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "human",
            "isRequired": True,
        },
        "Questionnaire.item.constraint.location": {
            "type": {"resourceType": "Entity", "id": "string"},
            "path": ["item", "constraint", "location"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "location",
            "isCollection": True,
        },
        "Questionnaire.item.constraint.expression": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "constraint", "expression"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "expression",
            "isRequired": True,
        },
        "Questionnaire.item.answerExpression": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "answerExpression"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerExpression",
            "description": "An expression (FHIRPath, CQL or FHIR Query) that resolves to a list of permitted answers for the question item or that establishes context for a group item."
        },
        "Questionnaire.item.calculatedExpression": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "calculatedExpression"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-calculatedExpression",
            "description": "Calculated value for a question answer as determined by an evaluated expression."
        },
        "Questionnaire.item.enableWhenExpression": {
            "type": {"resourceType": "Entity", "id": "Expression"},
            "path": ["item", "enableWhenExpression"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-enableWhenExpression",
            "description": "An expression that returns a boolean value for whether to enable the item."
        },
        "Questionnaire.item.referenceResource": {
            "type": {"resourceType": "Entity", "id": "code"},
            "path": ["item", "referenceResource"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/StructureDefinition/questionnaire-referenceResource",
            "isCollection": True,
            "description": "Where the type for a question is Reference, indicates a type of resource that is permitted."
        },
        "Questionnaire.item.choiceColumn": {
            "path": ["item", "choiceColumn"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-choiceColumn",
            "isCollection": True,
            "description": "Guide for rendering multi-column choices"
        },
        "Questionnaire.item.choiceColumn.path": {
            "type": {"resourceType": "Entity", "id": "string"},
            "path": ["item", "choiceColumn", "path"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "path",
            "isRequired": True,
            "description": "Column path",
        },
        "Questionnaire.item.choiceColumn.label": {
            "type": {"resourceType": "Entity", "id": "string"},
            "path": ["item", "choiceColumn", "label"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "label",
            "description": "Column label",
        },
        "Questionnaire.item.choiceColumn.width": {
            "type": {"resourceType": "Entity", "id": "Quantity"},
            "path": ["item", "choiceColumn", "width"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "width",
            "description": "Width of column",
        },
        "Questionnaire.item.choiceColumn.forDisplay": {
            "type": {"resourceType": "Entity", "id": "boolean"},
            "path": ["item", "choiceColumn", "forDisplay"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "forDisplay",
            "description": "Use for display ?"
        },
    },
}

updated_meta_resources_v3_0_0 = {
    "Attribute": {
        "Questionnaire.sourceQueries": {
            "type": {"resourceType": "Entity", "id": "Reference"},
            "path": ["sourceQueries"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
        },
        "Questionnaire.launchContext.name": {
            "type": {"resourceType": "Entity", "id": "id"},
            "path": ["launchContext", "name", "code"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "name",
        },
        "Questionnaire.launchContext.type": {
            "type": {"resourceType": "Entity", "id": "code"},
            "path": ["launchContext", "type", "0"],
            "resource": {"resourceType": "Entity", "id": "Questionnaire"},
            "extensionUrl": "type",
        },
    }
}

meta_resources_v3_0_0 = {
    "Attribute": {**meta_resources_v2_7_0["Attribute"], **updated_meta_resources_v3_0_0["Attribute"]}
}
