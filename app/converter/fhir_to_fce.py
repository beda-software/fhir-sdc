import copy

from fhirpy.base.utils import get_by_path


def to_first_class_extension(fhirResource):
    if fhirResource.get("resourceType") == "Questionnaire":
        fhirQuestionnaire = copy.deepcopy(fhirResource)
        # check_fhir_questionnaire_profile(fhirQuestionnaire)
        meta = process_meta_questionnaire(fhirQuestionnaire)
        item = process_items(fhirQuestionnaire)
        extensions = process_extension(fhirQuestionnaire)
        questionnaire = trim_empty(
            {**fhirQuestionnaire, "meta": meta, "item": item, "extension": None, **extensions}
        )

        return questionnaire
    elif fhirResource.get("resourceType") == "QuestionnaireResponse":
        questionnaireResponse = copy.deepcopy(fhirResource)
        process_answer_qr(questionnaireResponse.get("item", []))
        if questionnaireResponse.get("meta"):
            process_meta_qr(questionnaireResponse["meta"])
        process_reference(questionnaireResponse)

        return questionnaireResponse
    return fhirResource


def process_answer_qr(items):
    if not items:
        return

    def process_answer(answer):
        value_handlers = {
            "valueString": lambda value: {"string": value},
            "valueInteger": lambda value: {"integer": value},
            "valueBoolean": lambda value: {"boolean": value},
            "valueCoding": lambda value: {"Coding": value},
            "valueDate": lambda value: {"date": value},
            "valueDateTime": lambda value: {"dateTime": value},
            "valueReference": lambda value: {
                "Reference": {
                    "display": value["display"],
                    "id": value["reference"].split("/")[-1],
                    "resourceType": value["reference"].split("/")[0],
                }
            },
            "valueTime": lambda value: {"time": value},
        }

        for key, handler in value_handlers.items():
            if key in answer:
                value = answer.pop(key)
                answer["value"] = handler(value)

    for item in items:
        if "answer" in item:
            for answer in item["answer"]:
                process_answer(answer)
        if "item" in item:
            process_answer_qr(item["item"])


def process_meta_qr(meta):
    if meta and meta.get("extension"):
        for ext in meta["extension"]:
            if ext.get("url") == "ex:createdAt":
                meta["createdAt"] = ext.get("valueInstant")
                del ext["url"]
                del ext["valueInstant"]
        del meta["extension"]


def check_fhir_questionnaire_profile(fhir_questionnaire):
    if not (
        len(fhir_questionnaire.get("meta", {}).get("profile", [])) == 1
        and fhir_questionnaire.get("meta", {}).get("profile", [])[0]
        == "https://emr-core.beda.software/StructureDefinition/fhir-emr-questionnaire"
    ):
        raise ValueError("Only beda emr questionnaire supported")


def process_reference(fhirQuestionnaireResponse):
    if fhirQuestionnaireResponse.get("encounter", {}).get("reference"):
        resourceType, id = fhirQuestionnaireResponse["encounter"]["reference"].split("/")
        fhirQuestionnaireResponse["encounter"] = {
            "resourceType": resourceType,
            "id": id,
        }
    if fhirQuestionnaireResponse.get("source", {}).get("reference"):
        resourceType, id = fhirQuestionnaireResponse["source"]["reference"].split("/")
        fhirQuestionnaireResponse["source"] = {
            "resourceType": resourceType,
            "id": id,
        }


def get_created_at(fhir_questionnaire):
    meta_extension = next(
        (
            ext
            for ext in fhir_questionnaire.get("meta", {}).get("extension", [])
            if ext.get("url") == "ex:createdAt"
        ),
        None,
    )
    return {"createdAt": meta_extension["valueInstant"]} if meta_extension else {}


def process_meta_questionnaire(fhirQuestionnaire):
    createdAt = get_created_at(fhirQuestionnaire)
    return {**fhirQuestionnaire.get("meta", {}), **createdAt, "extension": None}


def process_items(fhirQuestionnaire):
    return (
        list(map(process_item, fhirQuestionnaire.get("item", [])))
        if "item" in fhirQuestionnaire
        else None
    )


def process_item(item):
    properties = {}

    updated_properties = get_updated_properties_from_item(item)
    properties = {**properties, **updated_properties}

    converted_item = convert_item_properties(item)

    new_item = {
        **converted_item,
        **properties,
        "extension": None,
    }

    if new_item.get("extension") is None:
        del new_item["extension"]

    if new_item.get("itemControl") is None:
        del new_item["itemControl"]

    return new_item


def process_extension(fhirQuestionnaire):
    launchContext = process_launch_context(fhirQuestionnaire)
    mapping = process_mapping(fhirQuestionnaire)
    source_queries = process_source_queries(fhirQuestionnaire)
    target_structure_map = process_target_structure_map(fhirQuestionnaire)
    item_population_context = find_extension(
        fhirQuestionnaire,
        "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
    )
    assemble_contexts = find_extensions(
        fhirQuestionnaire,
        "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-assembleContext",
    )

    return {
        "launchContext": launchContext if launchContext else None,
        "mapping": mapping if mapping else None,
        "sourceQueries": source_queries if source_queries else None,
        "targetStructureMap": target_structure_map if target_structure_map else None,
        "itemPopulationContext": (
            item_population_context["valueExpression"]
            if item_population_context
            else None
        ),
        "assembleContext": [
            assemble_context["valueString"] for assemble_context in assemble_contexts
        ] if assemble_contexts else None,
    }


def trim_empty(e):
    for prop, val in list(e.items()):
        if val is None or (isinstance(val, list) and len(val) == 0):
            del e[prop]
        elif isinstance(val, dict):
            trim_empty(val)
        elif isinstance(val, list):
            for i in range(len(val)):
                if isinstance(val[i], dict):
                    trim_empty(val[i])
    return e


def process_launch_context(fhir_questionnaire):
    launch_context_extensions = fhir_questionnaire.get("extension", [])

    launch_context_extensions = [
        ext
        for ext in launch_context_extensions
        if ext.get("url")
        == "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext"
    ]

    if not launch_context_extensions:
        return None

    result = []
    for launch_context_extension in launch_context_extensions:
        name_extension = next(
            (
                ext
                for ext in launch_context_extension.get("extension", [])
                if ext.get("url") == "name"
            ),
            None,
        )
        type_extension = next(
            (
                ext
                for ext in launch_context_extension.get("extension", [])
                if ext.get("url") == "type"
            ),
            None,
        )
        description_extension = next(
            (
                ext
                for ext in launch_context_extension.get("extension", [])
                if ext.get("url") == "description"
            ),
            None,
        )

        name = get_by_path(name_extension, ["valueCoding"])
        type_code = get_by_path(type_extension, ["valueCode"])
        description = get_by_path(description_extension, ["valueString"])

        context_found = False
        for context in result:
            if context["name"]["code"] == name["code"]:
                context["type"].append(type_code)
                context_found = True
                break

        if not context_found:
            context = {
                "name": name,
                "type": [type_code],
            }
            if description:
                context["description"] = description
            result.append(context)

    return result


def process_mapping(fhirQuestionnaire):
    mapperExtensions = list(
        filter(
            lambda ext: ext.get("url")
            == "https://emr-core.beda.software/StructureDefinition/questionnaire-mapper",
            fhirQuestionnaire.get("extension", []),
        )
    )

    if not mapperExtensions:
        return None

    return list(
        map(
            lambda mapperExtension: {
                "id": mapperExtension.get("valueReference", {}).get("reference", "").split("/")[1],
                "resourceType": "Mapping",
            },
            mapperExtensions,
        )
    )


def process_target_structure_map(fhirQuestionnaire):
    extensions = [
        extension
        for extension in fhirQuestionnaire.get("extension", [])
        if extension["url"]
        == "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-targetStructureMap"
    ]

    if not extensions:
        return None

    return [extension["valueCanonical"] for extension in extensions]


def get_updated_properties_from_item(item):
    updated_properties = {}

    hidden = find_extension(item, "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden")
    if hidden is not None:
        hidden = hidden["valueBoolean"]

    initial_expression = find_extension(
        item, "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression"
    )
    if initial_expression is not None:
        initial_expression = initial_expression["valueExpression"]

    item_population_context = find_extension(
        item,
        "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemPopulationContext",
    )
    if item_population_context is not None:
        item_population_context = item_population_context["valueExpression"]

    sub_questionnaire = find_extension(
        item, "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire"
    )
    if sub_questionnaire is not None:
        sub_questionnaire = sub_questionnaire["valueCanonical"]

    item_control = find_extension(
        item, "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl"
    )
    if item_control is not None:
        item_control = item_control["valueCodeableConcept"]

    item_inline_choice_direction = find_extension(
        item, "https://beda.software/fhir-emr-questionnaire/inline-choice-direction"
    )
    if item_inline_choice_direction is not None:
        item_inline_choice_direction = item_inline_choice_direction["valueString"]

    updated_properties["hidden"] = hidden
    updated_properties["initialExpression"] = initial_expression
    updated_properties["itemPopulationContext"] = item_population_context
    updated_properties["subQuestionnaire"] = sub_questionnaire
    updated_properties["itemControl"] = item_control
    updated_properties["inlineChoiceDirection"] = item_inline_choice_direction

    item_type = item.get("type", "")

    if item_type in ["string", "date", "dateTime"]:
        updated_properties["initial"] = [
            {"value": {"Coding": init["valueCoding"]}} if "valueCoding" in init else init
            for init in item.get("initial", [])
        ]

    if item_type == "choice":
        answer_option = item.get("answerOption", [])
        updated_properties["answerOption"] = []

        for option in answer_option:
            if "valueString" in option:
                updated_properties["answerOption"].append(
                    {"value": {"string": option["valueString"]}}
                )
            if "valueCoding" in option:
                updated_properties["answerOption"].append(
                    {
                        "value": {
                            "Coding": {
                                "code": option.get("valueCoding", {}).get("code"),
                                "display": option.get("valueCoding", {}).get("display"),
                                "system": option.get("valueCoding", {}).get("system"),
                            }
                        }
                    }
                )
            if "valueReference" in option:
                updated_properties["answerOption"].append(
                    {
                        "value": {
                            "Reference": {
                                "resourceType": option.get("valueReference", {}).get(
                                    "resourceType"
                                ),
                                "display": option.get("valueReference", {}).get("display"),
                                "extension": option.get("valueReference", {}).get("extension"),
                                "localRef": option.get("valueReference", {}).get("localRef"),
                                "resource": option.get("valueReference", {}).get("resource"),
                                "type": option.get("valueReference", {}).get("type"),
                                "uri": option.get("valueReference", {}).get("reference"),
                            }
                        }
                    }
                )
            if "valueDate" in option:
                updated_properties["answerOption"].append({"value": {"date": option["valueDate"]}})
            if "valueInteger" in option:
                updated_properties["answerOption"].append(
                    {"value": {"integer": option["valueInteger"]}}
                )
            if "valueTime" in option:
                updated_properties["answerOption"].append({"value": {"time": option["valueTime"]}})

        adjust_last_to_right = find_extension(
            item, "https://beda.software/fhir-emr-questionnaire/adjust-last-to-right"
        )
        if adjust_last_to_right is not None:
            updated_properties["adjustLastToRight"] = adjust_last_to_right["valueBoolean"]
        updated_properties["initial"] = [
            {"value": {"Coding": init["valueCoding"]}} if "valueCoding" in init else init
            for init in item.get("initial", [])
        ]

    enable_when = [process_enable_when_item(condition) for condition in item.get("enableWhen", [])]
    if len(enable_when) > 0:
        updated_properties["enableWhen"] = enable_when

    if item_type in ["decimal", "integer"]:
        slider_start = find_extension(
            item, "https://beda.software/fhir-emr-questionnaire/slider-start"
        )
        if slider_start is not None:
            updated_properties["start"] = slider_start["valueInteger"]
        slider_stop = find_extension(
            item, "https://beda.software/fhir-emr-questionnaire/slider-stop"
        )
        if slider_stop is not None:
            updated_properties["stop"] = slider_stop["valueInteger"]
        help_text = find_extension(item, "https://beda.software/fhir-emr-questionnaire/help-text")
        if help_text is not None:
            updated_properties["helpText"] = help_text["valueString"]
        stop_label = find_extension(
            item, "https://beda.software/fhir-emr-questionnaire/slider-stop-label"
        )
        if stop_label is not None:
            updated_properties["stopLabel"] = stop_label["valueString"]
        slider_step_value = find_extension(
            item, "http://hl7.org/fhir/StructureDefinition/questionnaire-sliderStepValue"
        )
        if slider_step_value is not None:
            updated_properties["sliderStepValue"] = slider_step_value["valueInteger"]

    if item_type == "integer":
        calculated_expression = find_extension(
            item,
            "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-calculatedExpression",
        )
        if calculated_expression is not None:
            updated_properties["calculatedExpression"] = calculated_expression["valueExpression"]

        unit = find_extension(item, "http://hl7.org/fhir/StructureDefinition/questionnaire-unit")
        if unit is not None:
            updated_properties["unit"] = unit["valueCoding"]

    if item_type == "text":
        macro = find_extension(item, "https://beda.software/fhir-emr-questionnaire/macro")
        if macro is not None:
            updated_properties["macro"] = macro["valueString"]

        enable_when_expression = find_extension(
            item,
            "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-enableWhenExpression",
        )
        if enable_when_expression is not None:
            updated_properties["enableWhenExpression"] = enable_when_expression["valueExpression"]

        enable_when = [
            process_enable_when_item(condition) for condition in item.get("enableWhen", [])
        ]
        if len(enable_when) > 0:
            updated_properties["enableWhen"] = enable_when

    if item_type == "group":
        if "item" in item:
            for nested_item in item["item"]:
                unit = find_extension(
                    nested_item, "http://hl7.org/fhir/StructureDefinition/questionnaire-unit"
                )
                if unit is not None:
                    nested_item["unit"] = unit["valueCoding"]

        enable_when = [
            process_enable_when_item(condition) for condition in item.get("enableWhen", [])
        ]
        if len(enable_when) > 0:
            updated_properties["enableWhen"] = enable_when

    if item_type == "boolean":
        boolean = find_initial_value(item, "valueBoolean")
        if boolean is not None:
            updated_properties["initial"] = [{"value": {"boolean": boolean}}]

    if item_type == "reference":
        choice_column_extension = find_extension(
            item, "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-choiceColumn"
        )
        if choice_column_extension is not None:
            choice_column_extension = choice_column_extension["extension"]
            for_display = next(
                (
                    obj["valueBoolean"]
                    for obj in choice_column_extension
                    if obj["url"] == "forDisplay"
                ),
                None,
            )
            path = next(
                (obj["valueString"] for obj in choice_column_extension if obj["url"] == "path"),
                None,
            )
            choice_column_array = [{"forDisplay": for_display or False, "path": path}]
            updated_properties["choiceColumn"] = choice_column_array

        answer_expression = find_extension(
            item,
            "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerExpression",
        )
        if answer_expression is not None:
            updated_properties["answerExpression"] = answer_expression["valueExpression"]

        reference_resource = find_extension(
            item, "http://hl7.org/fhir/StructureDefinition/questionnaire-referenceResource"
        )

        enable_when = [
            process_enable_when_item(condition) for condition in item.get("enableWhen", [])
        ]
        if len(enable_when) > 0:
            updated_properties["enableWhen"] = enable_when

        if reference_resource is not None:
            reference_resource_array = [reference_resource["valueCode"]]
            updated_properties["referenceResource"] = reference_resource_array

    if item_type == "display":
        help_text = find_extension(item, "https://beda.software/fhir-emr-questionnaire/help-text")
        if help_text is not None:
            updated_properties["helpText"] = help_text["valueString"]

    if item.get("initialExpression"):
        updated_properties["initialExpression"] = {
            "expression": item["initialExpression"]["expression"],
            "language": item["initialExpression"]["language"],
        }

    if item.get("itemPopulationContext"):
        updated_properties["itemPopulationContext"] = {
            "expression": item["itemPopulationContext"]["expression"],
            "language": item["itemPopulationContext"]["language"],
        }

    return updated_properties


def convert_item_properties(item):
    updated_properties = get_updated_properties_from_item(item)
    new_item = {**item, **updated_properties}
    if "extension" in new_item:
        del new_item["extension"]

    if new_item.get("item"):
        new_item["item"] = [
            convert_item_properties(nested_item) for nested_item in new_item["item"]
        ]

    return new_item


def process_source_queries(fhirQuestionnaire):
    extensions = list(
        filter(
            lambda ext: ext.get("url")
            == "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
            fhirQuestionnaire.get("extension", []),
        )
    )
    return list(
        map(
            lambda ext: {
                "localRef": get_by_path(ext, ["valueReference", "reference"], default="")[1:]
            },
            extensions,
        )
    )


def find_extensions(item, url):
    return [ext for ext in item.get("extension", []) if ext.get("url") == url]


def find_extension(item, url):
    try:
        return find_extensions(item, url)[0]
    except IndexError:
        return None


def find_initial_value(item, property):
    for init in item.get("initial", []):
        if init.get(property) is not None:
            return init.get(property)
    return None


def process_enable_when_item(item):
    question = item.get("question")
    operator = item.get("operator")
    answer = {}

    if "answerBoolean" in item:
        answer["boolean"] = item["answerBoolean"]
    elif "answerDecimal" in item:
        answer["decimal"] = item["answerDecimal"]
    elif "answerInteger" in item:
        answer["integer"] = item["answerInteger"]
    elif "answerDate" in item:
        answer["date"] = item["answerDate"]
    elif "answerDateTime" in item:
        answer["dateTime"] = item["answerDateTime"]
    elif "answerTime" in item:
        answer["time"] = item["answerTime"]
    elif "answerString" in item:
        answer["string"] = item["answerString"]
    elif "answerCoding" in item:
        answer["Coding"] = item["answerCoding"]
    elif "answerQuantity" in item:
        answer["Quantity"] = item["answerQuantity"]
    elif "answerReference" in item:
        reference = item["answerReference"]["reference"]
        split_reference = reference.split("/")
        answer["Reference"] = {
            **item["answerReference"],
            "id": split_reference[1],
            "resourceType": split_reference[0],
        }
        del answer["Reference"]["reference"]

    return {
        "question": question,
        "operator": operator,
        "answer": answer,
    }
