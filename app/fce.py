import copy

from fhirpy.base.utils import get_by_path


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


def find_extension(item, url):
    return next((ext for ext in item.get("extension", []) if ext.get("url") == url), None)


def find_initial_value(item, property):
    for init in item.get("initial", []):
        if init.get(property) is not None:
            return init.get(property)
    return None


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
    item_control = find_extension(
        item, "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl"
    )
    if item_control is not None:
        item_control = item_control["valueCodeableConcept"]

    updated_properties["hidden"] = hidden
    updated_properties["initialExpression"] = initial_expression
    updated_properties["itemControl"] = item_control

    item_type = item.get("type", "")

    if item_type in ["string", "date", "dateTime"]:
        updated_properties["initial"] = [
            {"value": {"Coding": init["valueCoding"]}} if "valueCoding" in init else init
            for init in item.get("initial", [])
        ]

    if item_type == "choice":
        answer_option = item.get("answerOption", [])
        updated_properties["answerOption"] = [
            {"value": {"string": option["valueString"]}}
            if "valueString" in option
            else {
                "value": {
                    "Coding": {
                        "code": option.get("valueCoding", {}).get("code"),
                        "display": option.get("valueCoding", {}).get("display"),
                        "system": option.get("valueCoding", {}).get("system"),
                    }
                }
            }
            for option in answer_option
            if "valueCoding" in option or "valueString" in option
        ]

        adjust_last_to_right = find_extension(
            item, "https://beda.software/fhir-emr-questionnaire/adjust-last-to-right"
        )
        if adjust_last_to_right is not None:
            updated_properties["adjustLastToRight"] = adjust_last_to_right["valueBoolean"]

        enable_when = [
            {
                "question": condition["question"],
                "operator": condition["operator"],
                "answer": {"Coding": condition["answerCoding"]},
            }
            for condition in item.get("enableWhen", [])
        ]
        if len(enable_when) > 0:
            updated_properties["enableWhen"] = enable_when

        updated_properties["initial"] = [
            {"value": {"Coding": init["valueCoding"]}} if "valueCoding" in init else init
            for init in item.get("initial", [])
        ]

    if item_type == "decimal":
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
            {
                "question": condition["question"],
                "operator": condition["operator"],
                "answer": {"boolean": condition["answerBoolean"]},
            }
            for condition in item.get("enableWhen", [])
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
            {
                "question": condition["question"],
                "operator": condition["operator"],
                "answer": {"boolean": condition["answerBoolean"]},
            }
            for condition in item.get("enableWhen", [])
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
        if reference_resource is not None:
            reference_resource_array = [reference_resource["valueCode"]]
            updated_properties["referenceResource"] = reference_resource_array

    if item.get("initialExpression"):
        updated_properties["initialExpression"] = {
            "expression": item["initialExpression"]["expression"],
            "language": item["initialExpression"]["language"],
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


def check_fhir_questionnaire_profile(fhir_questionnaire):
    if not (
        len(fhir_questionnaire.get("meta", {}).get("profile", [])) == 1
        and fhir_questionnaire.get("meta", {}).get("profile", [])[0]
        == "https://beda.software/beda-emr-questionnaire"
    ):
        raise ValueError("Only beda emr questionnaire supported")


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

        name_code = get_by_path(name_extension, ["valueCoding", "code"])
        type_code = get_by_path(type_extension, ["valueCode"])
        description = get_by_path(description_extension, ["valueString"])

        context = {
            "name": {
                "code": name_code,
            },
            "type": type_code,
        }

        if description:
            context["description"] = description

        result.append(context)

    return result


def processMapping(fhirQuestionnaire):
    mapperExtensions = list(
        filter(
            lambda ext: ext.get("url")
            == "http://beda.software/fhir-extensions/questionnaire-mapper",
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


def processMeta(fhirQuestionnaire):
    createdAt = get_created_at(fhirQuestionnaire)
    return {**fhirQuestionnaire.get("meta", {}), **createdAt, "extension": None}


def processItems(fhirQuestionnaire):
    return (
        list(map(process_item, fhirQuestionnaire.get("item", [])))
        if "item" in fhirQuestionnaire
        else None
    )


def processExtensions(fhirQuestionnaire):
    launchContext = process_launch_context(fhirQuestionnaire)
    mapping = processMapping(fhirQuestionnaire)

    return {
        "launchContext": launchContext if launchContext and len(launchContext) else None,
        "mapping": mapping if mapping and len(mapping) else None,
    }


def processAnswerToFCE(itemList):
    if not itemList:
        return
    for item in itemList:
        if item.get("answer") and item.get("answer")[0].get("valueString"):
            item["answer"][0]["value"] = {"string": item["answer"][0].get("valueString")}
            del item["answer"][0]["valueString"]
        elif item.get("answer") and item.get("answer")[0].get("valueInteger"):
            item["answer"][0]["value"] = {"integer": item["answer"][0].get("valueInteger")}
            del item["answer"][0]["valueInteger"]
        elif item.get("answer") and item.get("answer")[0].get("valueBoolean"):
            item["answer"][0]["value"] = {"boolean": item["answer"][0].get("valueBoolean")}
            del item["answer"][0]["valueBoolean"]
        elif item.get("answer") and item.get("answer")[0].get("valueCoding"):
            item["answer"][0]["value"] = {"Coding": item["answer"][0].get("valueCoding")}
            del item["answer"][0]["valueCoding"]
        elif item.get("answer") and item.get("answer")[0].get("valueDate"):
            item["answer"][0]["value"] = {"date": item["answer"][0].get("valueDate")}
            del item["answer"][0]["valueDate"]
        elif item.get("answer") and item.get("answer")[0].get("valueDateTime"):
            item["answer"][0]["value"] = {"dateTime": item["answer"][0].get("valueDateTime")}
            del item["answer"][0]["valueDateTime"]
        elif item.get("answer") and item.get("answer")[0].get("valueReference"):
            display = item["answer"][0]["valueReference"].get("display")
            resource = item["answer"][0]["valueReference"].get("resource")
            resourceType = resource.get("resourceType")
            item["answer"][0]["value"] = {
                "Reference": {
                    "display": display,
                    "id": resource.get("id"),
                    "resource": resource,
                    "resourceType": resourceType,
                }
            }
            del item["answer"][0]["valueReference"]
        elif item.get("answer") and item.get("answer")[0].get("valueTime"):
            item["answer"][0]["value"] = {"time": item["answer"][0].get("valueTime")}
            del item["answer"][0]["valueTime"]
        elif item.get("item"):
            processAnswerToFCE(item.get("item"))


def processAnswerToFHIR(itemList):
    if not itemList:
        return
    for item in itemList:
        if (
            item.get("answer")
            and item.get("answer")[0].get("value")
            and item.get("answer")[0]["value"].get("string")
        ):
            item["answer"][0]["valueString"] = item["answer"][0]["value"]["string"]
            del item["answer"][0]["value"]
        elif (
            item.get("answer")
            and item.get("answer")[0].get("value")
            and item.get("answer")[0]["value"].get("integer")
        ):
            item["answer"][0]["valueInteger"] = item["answer"][0]["value"]["integer"]
            del item["answer"][0]["value"]
        elif (
            item.get("answer")
            and item.get("answer")[0].get("value")
            and item.get("answer")[0]["value"].get("boolean")
        ):
            item["answer"][0]["valueBoolean"] = item["answer"][0]["value"]["boolean"]
            del item["answer"][0]["value"]
        elif (
            item.get("answer")
            and item.get("answer")[0].get("value")
            and item.get("answer")[0]["value"].get("Coding")
        ):
            item["answer"][0]["valueCoding"] = item["answer"][0]["value"]["Coding"]
            del item["answer"][0]["value"]
        elif (
            item.get("answer")
            and item.get("answer")[0].get("value")
            and item.get("answer")[0]["value"].get("date")
        ):
            item["answer"][0]["valueDate"] = item["answer"][0]["value"]["date"]
            del item["answer"][0]["value"]
        elif (
            item.get("answer")
            and item.get("answer")[0].get("value")
            and item.get("answer")[0]["value"].get("dateTime")
        ):
            item["answer"][0]["valueDateTime"] = item["answer"][0]["value"]["dateTime"]
            del item["answer"][0]["value"]
        elif (
            item.get("answer")
            and item.get("answer")[0].get("value")
            and item.get("answer")[0]["value"].get("Reference")
        ):
            display = item["answer"][0]["value"]["Reference"].get("display")
            resource = item["answer"][0]["value"]["Reference"].get("resource")
            resourceType = item["answer"][0]["value"]["Reference"].get("resourceType")
            id = item["answer"][0]["value"]["Reference"].get("id")
            item["answer"][0]["valueReference"] = {
                "display": display,
                "resource": resource,
                "reference": f"{resourceType}/{id}",
            }
            del item["answer"][0]["value"]
        elif (
            item.get("answer")
            and item.get("answer")[0].get("value")
            and item.get("answer")[0]["value"].get("time")
        ):
            item["answer"][0]["valueTime"] = item["answer"][0]["value"]["time"]
            del item["answer"][0]["value"]
        elif item.get("item"):
            processAnswerToFHIR(item["item"])


def processMetaToFCE(meta):
    if meta and meta.get("extension"):
        for ext in meta["extension"]:
            if ext.get("url") == "ex:createdAt":
                meta["createdAt"] = ext.get("valueInstant")
                del ext["url"]
                del ext["valueInstant"]
        del meta["extension"]


def processMetaToFHIR(meta):
    if meta and meta.get("createdAt"):
        meta["extension"] = [{"url": "ex:createdAt", "valueInstant": meta["createdAt"]}]
        del meta["createdAt"]


def processReferenceToFCE(fhirQuestionnaireResponse):
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


def processReferenceToFHIR(fceQR):
    if fceQR.get("encounter", {}).get("resourceType") and fceQR["encounter"].get("id"):
        fceQR["encounter"][
            "reference"
        ] = f"{fceQR['encounter']['resourceType']}/{fceQR['encounter']['id']}"
        del fceQR["encounter"]["resourceType"]
        del fceQR["encounter"]["id"]
    if fceQR.get("source", {}).get("resourceType") and fceQR["source"].get("id"):
        fceQR["source"]["reference"] = f"{fceQR['source']['resourceType']}/{fceQR['source']['id']}"
        del fceQR["source"]["resourceType"]
        del fceQR["source"]["id"]


def to_first_class_extension(fhirResource):
    if fhirResource.get("resourceType") == "Questionnaire":
        fhirQuestionnaire = copy.deepcopy(fhirResource)
        check_fhir_questionnaire_profile(fhirQuestionnaire)
        meta = processMeta(fhirQuestionnaire)
        item = processItems(fhirQuestionnaire)
        extensions = processExtensions(fhirQuestionnaire)
        questionnaire = trim_empty(
            {
                **fhirQuestionnaire,
                "meta": meta,
                "item": item,
                "launchContext": extensions["launchContext"],
                "mapping": extensions["mapping"],
                "extension": None,
            }
        )
        return questionnaire
    elif fhirResource.get("resourceType") == "QuestionnaireResponse":
        questionnaireResponse = copy.deepcopy(fhirResource)
        processAnswerToFCE(questionnaireResponse.get("item", []))
        if questionnaireResponse.get("meta"):
            processMetaToFCE(questionnaireResponse["meta"])
        processReferenceToFCE(questionnaireResponse)
        return questionnaireResponse


def from_first_class_extension(fceResource):
    if fceResource.get("resourceType") == "Questionnaire":
        questionnaire = copy.deepcopy(fceResource)
        processMetaToFHIR(questionnaire.get("meta"))
        process_items_to_fhir(questionnaire.get("item"))
        processExtensionsToFHIR(questionnaire)
        return questionnaire
    elif fceResource.get("resourceType") == "QuestionnaireResponse":
        questionnaireResponse = copy.deepcopy(fceResource)
        processAnswerToFHIR(questionnaireResponse.get("item", []))
        processMetaToFHIR(questionnaireResponse.get("meta"))
        processReferenceToFHIR(questionnaireResponse)
        return questionnaireResponse
    return fceResource


def process_items_to_fhir(items):
    if not items:
        return

    for item in items:
        if item.get("item"):
            process_items_to_fhir(item["item"])

        if item.get("macro"):
            macro_extension = {
                "url": "https://beda.software/fhir-emr-questionnaire/macro",
                "valueString": item["macro"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(macro_extension)
            del item["macro"]

        if item.get("itemControl"):
            item_control_extension = {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                "valueCodeableConcept": {
                    "coding": item["itemControl"]["coding"],
                },
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(item_control_extension)
            del item["itemControl"]

        if item.get("start") is not None:
            start_extension = {
                "url": "https://beda.software/fhir-emr-questionnaire/slider-start",
                "valueInteger": item["start"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(start_extension)
            del item["start"]

        if item.get("stop") is not None:
            stop_extension = {
                "url": "https://beda.software/fhir-emr-questionnaire/slider-stop",
                "valueInteger": item["stop"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(stop_extension)
            del item["stop"]

        if item.get("helpText") is not None:
            help_text_extension = {
                "url": "https://beda.software/fhir-emr-questionnaire/help-text",
                "valueString": item["helpText"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(help_text_extension)
            del item["helpText"]

        if item.get("stopLabel") is not None:
            stop_label_extension = {
                "url": "https://beda.software/fhir-emr-questionnaire/slider-stop-label",
                "valueString": item["stopLabel"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(stop_label_extension)
            del item["stopLabel"]

        if item.get("sliderStepValue") is not None:
            slider_step_value_extension = {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-sliderStepValue",
                "valueInteger": item["sliderStepValue"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(slider_step_value_extension)
            del item["sliderStepValue"]

        if item.get("adjustLastToRight") is not None:
            adjust_last_to_right_extension = {
                "url": "https://beda.software/fhir-emr-questionnaire/adjust-last-to-right",
                "valueBoolean": item["adjustLastToRight"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(adjust_last_to_right_extension)
            del item["adjustLastToRight"]

        if item.get("answerOption"):
            for option in item["answerOption"]:
                if "value" in option and "Coding" in option["value"]:
                    option["valueCoding"] = option["value"]["Coding"]
                    del option["value"]
                elif "value" in option and "string" in option["value"]:
                    option["valueString"] = option["value"]["string"]
                    del option["value"]

        if item.get("hidden") is not None:
            hidden_extension = {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                "valueBoolean": item["hidden"],
            }
            item["extension"] = item.get("extension", []) + [hidden_extension]
            del item["hidden"]

        if item.get("enableWhen") is not None:
            enableWhen = []
            for condition in item["enableWhen"]:
                result = {"question": condition["question"], "operator": condition["operator"]}
                if "answer" in condition:
                    answer_coding = condition["answer"].get("Coding")
                    answer_boolean = condition["answer"].get("boolean")
                    if answer_coding:
                        result["answerCoding"] = answer_coding
                    elif answer_boolean is not None:
                        result["answerBoolean"] = answer_boolean
                enableWhen.append(result)
            item["enableWhen"] = enableWhen

        if item.get("initialExpression") is not None:
            extension = {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                "valueExpression": item["initialExpression"],
            }
            item["extension"] = item.get("extension", []) + [extension]
            del item["initialExpression"]

        if item.get("initial"):
            item["initial"] = [
                {"valueBoolean": entry["value"]["boolean"]}
                if "boolean" in entry["value"]
                else {"valueCoding": entry["value"]["Coding"]}
                for entry in item["initial"]
            ]

        if item.get("choiceColumn"):
            extension = {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-choiceColumn",
                "extension": [],
            }
            for column in item["choiceColumn"]:
                if isinstance(column.get("path"), str):
                    extension["extension"].append({"url": "path", "valueString": column["path"]})
                if isinstance(column.get("forDisplay"), bool):
                    extension["extension"].append(
                        {"url": "forDisplay", "valueBoolean": column["forDisplay"]}
                    )
            if extension["extension"]:
                item["extension"] = item.get("extension", []) + [extension]
            del item["choiceColumn"]

        if item.get("answerExpression"):
            extension = {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerExpression",
                "valueExpression": item["answerExpression"],
            }
            item["extension"] = item.get("extension", []) + [extension]
            del item["answerExpression"]

        if item.get("referenceResource"):
            reference_resource_extension = {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-referenceResource",
                "valueCode": item["referenceResource"][0],
            }
            item["extension"] = item.get("extension", []) + [reference_resource_extension]
            del item["referenceResource"]

        if item.get("unit"):
            unitExtension = {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                "valueCoding": item["unit"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(unitExtension)
            del item["unit"]

        if item.get("calculatedExpression"):
            calculatedExpressionExtension = {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-calculatedExpression",
                "valueExpression": {
                    "language": item["calculatedExpression"]["language"],
                    "expression": item["calculatedExpression"]["expression"],
                },
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(calculatedExpressionExtension)
            del item["calculatedExpression"]

        if item.get("enableWhenExpression"):
            enableWhenExpression = {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-enableWhenExpression",
                "valueExpression": {
                    "language": "text/fhirpath",
                    "expression": item["enableWhenExpression"]["expression"],
                },
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(enableWhenExpression)
            del item["enableWhenExpression"]


def processExtensionsToFHIR(questionnaire):
    if questionnaire.get("launchContext"):
        extension = []
        for launchContext in questionnaire.get("launchContext"):
            name = launchContext.get("name").get("code")
            type_ = launchContext.get("type")
            description = launchContext.get("description")

            launch_context_extension = [
                {"url": "name", "valueId": {"code": name}},
                {"url": "type", "valueCode": type_},
            ]

            if description is not None:
                launch_context_extension.append({"url": "description", "valueString": description})

            extension.append(
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
                    "extension": launch_context_extension,
                }
            )

        questionnaire["extension"] = questionnaire.get("extension", [])
        questionnaire["extension"].extend(extension)
        del questionnaire["launchContext"]

    if questionnaire.get("mapping"):
        mapping_extension = {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": f"Mapping/{questionnaire.get('mapping')[0].get('id')}"},
        }
        questionnaire["extension"] = questionnaire.get("extension", [])
        questionnaire["extension"].append(mapping_extension)
        del questionnaire["mapping"]

    if questionnaire.get("assembledFrom"):
        assembled_from_extension = {
            "url": "https://jira.hl7.org/browse/FHIR-22356#assembledFrom",
            "valueCanonical": questionnaire.get("assembledFrom"),
        }
        questionnaire["extension"] = questionnaire.get("extension", [])
        questionnaire["extension"].append(assembled_from_extension)
        del questionnaire["assembledFrom"]

    def process_item(item):
        if "item" in item:
            for sub_item in item["item"]:
                process_item(sub_item)

        if item.get("itemContext"):
            item_context_extension = {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemContext",
                "valueExpression": item["itemContext"],
            }
            item["extension"] = item.get("extension", [])
            item["extension"].append(item_context_extension)
            del item["itemContext"]

    if "item" in questionnaire:
        for item in questionnaire["item"]:
            process_item(item)
