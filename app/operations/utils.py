from fhirpathpy import evaluate as fhirpath
from fhirpy.base.utils import get_by_path
from funcy.seqs import first
from funcy.strings import re_all
from funcy.types import is_list, is_mapping


def get_type(item, data):
    type = item["type"]
    if type == "choice":
        option_type = get_by_path(item, ["answerOption", 0, "value"])
        if option_type:
            type = next(iter(option_type.keys()))
        else:
            type = "Coding"
        if isinstance(data[0], str):
            return "string"
    elif type == "text":
        type = "string"
    elif type == "attachment":
        type = "Attachment"
    elif type == "email":
        type = "string"
    elif type == "phone":
        type = "string"
    elif type == "display":
        type = "string"
    elif type == "reference":
        type = "Reference"

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


def pp(i, env, force):
    if not isinstance(i, str):
        return i
    exprs = re_all(r"(?P<var>{{[\S\s]+?}})", i)
    vs = {}
    for exp in exprs:
        data = fhirpath({}, exp["var"][2:-2], env)
        if len(data) > 0:
            vs[exp["var"]] = data[0]
        elif force:
            vs[exp["var"]] = ""
    res = i
    for k, v in vs.items():
        res = res.replace(k, v)

    return res


def prepare_bundle(raw_bundle, env, force=False):
    return walk_dict(raw_bundle, lambda i: pp(i, env, force))


def prepare_variables(item):
    variables = {}
    for var in item.get("variable", []):
        variables[var["name"]] = fhirpath({}, var["expression"])
    return variables


def parameter_to_env(resource):
    env = {}
    for param in resource["parameter"]:
        if "resource" in param:
            env[param["name"]] = param["resource"]
        else:
            value = param["value"]
            polimorphic_key = first(value.keys())
            if polimorphic_key:
                env[param["name"]] = value[polimorphic_key]
    return env


async def load_source_queries(sdk, questionnaire, env):
    contained = {
        f"{item['resourceType']}#{item['id']}": item for item in questionnaire.get("contained", [])
    }

    for source_query in questionnaire.get("sourceQueries", []):
        if "localRef" in source_query:
            raw_bundle = contained[source_query["localRef"]]
            if raw_bundle:
                bundle = prepare_bundle(raw_bundle, env, force=True)
                env[bundle["id"]] = await sdk.client.execute("/", data=bundle)


def update_link_ids(d, variables=None):
    variables = variables or {}
    for k, v in d.items():
        if is_list(v):
            d[k] = [update_link_ids(vi, variables) for vi in v]
        elif is_mapping(v):
            d[k] = update_link_ids(v, variables)
        else:
            # TODO it seems that it smells bed
            if k in ["linkId", "question"]:
                d[k] = update_link_id(v, variables)
    return d


def update_link_id(item, variables):
    if not isinstance(item, str):
        return item
    exprs = re_all(r"(?P<var>{{[\S\s]+?}})", item)
    vs = {}
    for exp in exprs:
        data = fhirpath({}, exp["var"][2:-2], variables)
        if len(data) > 0:
            vs[exp["var"]] = data[0]
    res = item
    for k, v in vs.items():
        res = res.replace(k, v)

    return res
