import copy

import json
from urllib.parse import quote

from fhirpathpy.models import models
from fhirpy.base.utils import get_by_path
from fpml import resolve_template
from funcy.seqs import first
from funcy.strings import re_all
from funcy.types import is_list, is_mapping

from app.cached_fhirpath import fhirpath
from .exception import ConstraintCheckOperationOutcome

r4 = models["r4"]


def get_type(item, data):
    type = item["type"]
    if type == "choice" or type == "open-choice":
        option_type = get_by_path(item, ["answerOption", 0, "value"])
        if option_type:
            type = next(iter(option_type.keys()))
        else:
            type = "Coding"
        if isinstance(data[0], str):
            return "string"
    elif type == "text":
        type = "string"
    elif type == "integer":
        type = "integer"
    elif type == "decimal":
        type = "decimal"
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
    elif type == "quantity":
        type = "Quantity"

    return type


def walk_dict(d, transform):
    result_dict = copy.deepcopy(d)
    for k, v in result_dict.items():
        if is_list(v):
            result_dict[k] = [
                walk_dict(vi, transform) if is_mapping(vi) else transform(vi, k) for vi in v
            ]
        elif is_mapping(v):
            result_dict[k] = walk_dict(v, transform)
        else:
            result_dict[k] = transform(v, k)
    return result_dict


def update_link_id_or_question(variables):
    def _update_link_id_or_question(value, key):
        if key in ["linkId", "question"]:
            return resolve_string_template(value, variables)
        else:
            return value

    return _update_link_id_or_question


def prepare_link_ids(questionnaire, variables):
    return walk_dict(questionnaire, update_link_id_or_question(variables))


def prepare_bundle(raw_bundle, env):
    return walk_dict(raw_bundle, lambda v, _k: resolve_string_template(v, env, encode_result=True))


def resolve_string_template(i, env, encode_result=False):
    if not isinstance(i, str):
        return i
    exprs = re_all(r"(?P<var>{{[\S\s]+?}})", i)
    vs = {}
    for exp in exprs:
        data = fhirpath({}, exp["var"][2:-2], env)
        if len(data) > 0:
            # NOTE: http://build.fhir.org/ig/HL7/sdc/expressions.html#x-fhir-query-enhancements
            # If the expression resolves to a collection of more than one value,
            # the substitution will be a list of comma-separated values (i.e. behaving as 'or').
            search_str = ",".join([str(item) for item in data])
            vs[exp["var"]] = quote(search_str) if encode_result else search_str
        else:
            vs[exp["var"]] = ""
    res = i
    for k, v in vs.items():
        res = res.replace(k, v)

    return res


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
            _name_key, value_key = param.keys()
            param_value = param[value_key]
            try:
                param_value = json.loads(param_value)
                polimorphic_key = first(param_value.keys())
                if polimorphic_key:
                    env[param["name"]] = param_value[polimorphic_key]
            except (json.JSONDecodeError, AttributeError):
                env[param["name"]] = param_value
    # Mapping parameters to fhir resource names
    questionnaire = env.get("questionnaire")
    if questionnaire:
        env["Questionnaire"] = questionnaire
    questionnaire_response = env.get("questionnaire_response")
    if questionnaire_response:
        env["QuestionnaireResponse"] = questionnaire_response
    return env


async def load_source_queries(client, fce_questionnaire, env):
    # Previously we used invalid format for localRef Bundle#id
    # But according to the specification, local ref to contained resource should be #id
    # And since in Aidbox format we have localRef without leading #, 
    # contained resources are accessible via id
    # But for backward compatibility they are also accessible by Bundle#id
    contained_compat = {
        f"{item['resourceType']}#{item['id']}": item
        for item in fce_questionnaire.get("contained", [])
    }
    contained_new = {
        item['id']: item
        for item in fce_questionnaire.get("contained", [])
    }
    contained = {**contained_compat, **contained_new}

    source_queries = fce_questionnaire.get("sourceQueries", {})

    if isinstance(source_queries, dict):
        source_queries = [source_queries]

    for source_query in source_queries:
        if "localRef" in source_query:
            raw_bundle = contained[source_query["localRef"]]
            if raw_bundle:
                bundle = prepare_bundle(raw_bundle, env)
                env[bundle["id"]] = await client.execute("/", data=bundle)


def validate_assemble_context(assemble_context: list[str], env):
    errors = []
    for var_name in assemble_context:
        if var_name not in env.keys():
            errors.append(
                {
                    "severity": "error",
                    "key": "undefined-var",
                    "human": "Context variable {} not defined".format(var_name),
                }
            )
    if len(errors) > 0:
        raise ConstraintCheckOperationOutcome(errors)   

def validate_context(context_definition, env):
    all_vars = env.keys()
    errors = []
    for item in context_definition:
        name = item["name"]
        if not isinstance(name, str):
            name = item["name"]["code"]
        if name not in all_vars:
            errors.append(
                {
                    "severity": "error",
                    "key": "undefined-var",
                    "human": "Context variable {} not defined".format(name),
                }
            )
    if len(errors) > 0:
        raise ConstraintCheckOperationOutcome(errors)


def check_mappers_bundles_full_url_duplicates(flattened_mappers_bundles):
    full_urls_set = set()

    for bundle in flattened_mappers_bundles:
        full_url = bundle.get("fullUrl")

        if full_url is None:
            continue

        if full_url in full_urls_set:
            raise ConstraintCheckOperationOutcome(
                [
                    {
                        "severity": "error",
                        "key": "duplicate-full-url",
                        "human": f"Duplicate fullUrl '{full_url}' in mappers bundles",
                    }
                ]
            )

        full_urls_set.add(full_url)


def answers(inputs, link_id):
    return fhirpath(
        inputs,
        f"repeat(item).where(linkId='{link_id}').answer.value",
        None,
        "r4",
    )


fp_options = {
    "userInvocationTable": {
        "answers": {
            "fn": answers,
            "arity": {0: [], 1: ["String"]},
        },
    },
    "model": r4,
}


def resolve_fpml_template(template, context):
    return resolve_template(
        context.get("QuestionniareResponse", context),
        template,
        context,
        fp_options,
        True,
    )


async def apply_converter_for_resources(converter_fn, resources: list) -> list:
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": dict(s)} for s in resources],
    }
    fce_bundle = await converter_fn(bundle)
    result = [s["resource"] for s in fce_bundle["entry"]]
    return result
