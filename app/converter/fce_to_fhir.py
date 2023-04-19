import copy


def from_first_class_extension(fceResource):
    if fceResource.get("resourceType") == "Questionnaire":
        questionnaire = copy.deepcopy(fceResource)
        process_meta_to_fhir(questionnaire.get("meta"))
        process_items_to_fhir(questionnaire.get("item"))
        process_extension_to_fhir(questionnaire)
        return questionnaire
    elif fceResource.get("resourceType") == "QuestionnaireResponse":
        questionnaireResponse = copy.deepcopy(fceResource)
        process_answer_to_fhir(questionnaireResponse.get("item", []))
        process_meta_to_fhir(questionnaireResponse.get("meta"))
        process_reference_to_fhir(questionnaireResponse)
        return questionnaireResponse
    return fceResource


def process_answer_to_fhir(items):
    if not items:
        return

    def process_answer(answer_item):
        if "value" not in answer_item:
            return
        value = answer_item["value"]
        value_mappings = {
            "string": "valueString",
            "integer": "valueInteger",
            "boolean": "valueBoolean",
            "Coding": "valueCoding",
            "date": "valueDate",
            "dateTime": "valueDateTime",
            "time": "valueTime",
        }
        for key, new_key in value_mappings.items():
            if key in value:
                answer_item[new_key] = value[key]
                del answer_item["value"]
                break
        if "Reference" in value:
            answer_item["valueReference"] = {
                "display": value["Reference"]["display"],
                "resource": value["Reference"]["resource"],
                "reference": f"{value['Reference']['resourceType']}/{value['Reference']['id']}",
            }
            del answer_item["value"]

    for item in items:
        if "answer" in item:
            for answer in item["answer"]:
                process_answer(answer)
        if "item" in item:
            process_answer_to_fhir(item["item"])


def process_meta_to_fhir(meta):
    if meta and meta.get("createdAt"):
        meta["extension"] = [{"url": "ex:createdAt", "valueInstant": meta["createdAt"]}]
        del meta["createdAt"]


def process_reference_to_fhir(fceQR):
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


def process_extension_to_fhir(questionnaire):
    process_launch_context(questionnaire)
    process_mapping(questionnaire)
    process_assebled_from(questionnaire)
    process_source_queries(questionnaire)

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


def process_launch_context(questionnaire):
    if "launchContext" in questionnaire:
        extension = []
        for launchContext in questionnaire["launchContext"]:
            name = launchContext["name"]["code"]
            type_list = launchContext["type"]
            description = launchContext.get("description")

            for type_code in type_list:
                launch_context_extension = [
                    {
                        "url": "name",
                        "valueCoding": {
                            "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                            "code": name,
                        },
                    },
                    {"url": "type", "valueCode": type_code},
                ]

                if description is not None:
                    launch_context_extension.append(
                        {"url": "description", "valueString": description}
                    )

                extension.append(
                    {
                        "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
                        "extension": launch_context_extension,
                    }
                )

        questionnaire["extension"] = questionnaire.get("extension", [])
        questionnaire["extension"].extend(extension)
        del questionnaire["launchContext"]


def process_mapping(questionnaire):
    if "mapping" in questionnaire:
        mapping = questionnaire["mapping"]
        for item in mapping:
            mapping_extension = {
                "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
                "valueReference": {"reference": f"Mapping/{item['id']}"},
            }
            questionnaire["extension"] = questionnaire.get("extension", [])
            questionnaire["extension"].append(mapping_extension)
        del questionnaire["mapping"]


def process_assebled_from(questionnaire):
    if questionnaire.get("assembledFrom"):
        assembled_from_extension = {
            "url": "https://jira.hl7.org/browse/FHIR-22356#assembledFrom",
            "valueCanonical": questionnaire.get("assembledFrom"),
        }
        questionnaire["extension"] = questionnaire.get("extension", [])
        questionnaire["extension"].append(assembled_from_extension)
        del questionnaire["assembledFrom"]


def process_source_queries(questionnaire):
    if "sourceQueries" in questionnaire:
        source_queries = questionnaire["sourceQueries"]
        for item in source_queries:
            extension = {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
                "valueReference": {"reference": f"#{item['localRef']}"},
            }
            questionnaire["extension"] = questionnaire.get("extension", [])
            questionnaire["extension"].append(extension)
        del questionnaire["sourceQueries"]
