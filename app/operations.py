import logging

from aiohttp import ClientSession, web
from fhirpathpy import evaluate as fhirpath
from fhirpy.utils import get_by_path
from funcy import is_list, is_mapping, re_all

from app.sdk import sdk


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"], public=True)
async def extract_questionnaire(operation, request):
    questionnaire_response = sdk.client.resource(
        "QuestionnaireResponse", **request["resource"]
    )
    questionnaire = (
        await sdk.client.resources("Questionnaire")
        .search(id=request["route-params"]["id"])
        .get()
    )
    resp = []
    for mapper in questionnaire["mapping"]:
        resp.append(
            await sdk.client._do_request(
                "post", f"Mapping/{mapper.id}/$apply", data=questionnaire_response
            )
        )

    return web.json_response(resp)


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$populate"])
async def populate_questionnaire_aidbox(operation, request):
    resource = request["resource"]
    env = {}
    for param in resource["parameter"]:
        if "resource" in param:
            env[param["name"]] = param["resource"]

    questionnaire = await sdk.client.resources("Questionnaire").get(
        id=request["route-params"]["id"]
    )

    contained = {
        f"{item.resourceType}#{item.id}": item
        for item in questionnaire.get("contained", [])
    }

    for source_query in questionnaire.get("sourceQueries", []):
        if "localRef" in source_query:
            raw_bundle = contained[source_query["localRef"]]
            if raw_bundle:
                bundle = prepare_bundle(raw_bundle, env)
                env[bundle.id] = await sdk.client._do_request("post", "/", data=bundle)

    root = {
        "resourceType": "QuestionnaireResponse",
        "questionnaire": request["route-params"]["id"],
        "item": [],
    }
    for item in questionnaire["item"]:
        root["item"].append(handle_item(item, env, {}))

    return web.json_response(root)


def handle_item(item, env, context):
    root = {"linkId": item["linkId"]}
    if "text" in item:
        root["text"] = item["text"]
    if "itemContext" in item:
        data = fhirpath(context, item["itemContext"]["expression"], env)
        context = data
    if (
        context
        and "initialExpression" in item
        and "repeats" in item
        and item["repeats"] is True
    ):
        answers = []
        root["answer"] = answers
        for index, _item in enumerate(context):
            type = get_type(item)
            data = fhirpath(
                context,
                "%context[{}].{}".format(
                    index, item["initialExpression"]["expression"]
                ),
                env,
            )
            answers.append({"value": {item["type"]: data[0]}})
    elif "initialExpression" in item:
        data = fhirpath(context, item["initialExpression"]["expression"], env)
        if data and len(data):
            type = get_type(item)
            if item.get("repeats") is True:
                root["answer"] = [{"value": {type: d}} for d in data]
            else:
                root["answer"] = [{"value": {type: data[0]}}]

    if (
        item["type"] == "group"
        and "repeats" in item
        and item["repeats"] is True
        and is_list(context)
    ):
        answer = []
        for c in context:
            q = []
            for i in item["item"]:
                q.append(handle_item(i, env, c))
            answer.append({"item": q})
        root["answer"] = answer

    elif "item" in item:
        root["item"] = []
        for i in item["item"]:
            root["item"].append(handle_item(i, env, context))

    return root


def get_type(item):
    type = item["type"]
    if type == "choice":
        option_type = get_by_path(item, ["answerOption", 0, "value"])
        if option_type:
            type = next(iter(option_type.keys()))
        else:
            type = "Coding"
    elif type == "text":
        type = "string"
    elif type == "attachment":
        type = "Attachment"
    elif type == "email":
        type = "string"
    elif type == "phone":
        type = "string"

    return type


def walk_dict(d, transform):
    for k, v in d.items():
        if is_list(v):
            d[k] = [walk_dict(vi, transform) for vi in v]
        elif is_mapping(v):
            d[k] = walk_dict(v, transform)
        else:
            d[k] = transform(v)
    return d


def prepare_bundle(raw_bundle, env):
    def pp(i):
        if not isinstance(i, str):
            return i
        exprs = re_all(r"(?P<var>{{[\S\s]+}})", i)
        vs = {}
        for exp in exprs:
            data = fhirpath({}, exp["var"][2:-2], env)
            if len(data) > 0:
                vs[exp["var"]] = data[0]

        res = i
        for k, v in vs.items():
            res = res.replace(k, v)

        return res

    return walk_dict(raw_bundle, pp)
