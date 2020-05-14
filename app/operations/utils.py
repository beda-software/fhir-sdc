from fhirpathpy import evaluate as fhirpath
from fhirpy.base.utils import get_by_path
from funcy.strings import re_all
from funcy.types import is_list, is_mapping


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


def parameter_to_env(resource):
    env = {}
    for param in resource["parameter"]:
        if "resource" in param:
            env[param["name"]] = param["resource"]
    return env
