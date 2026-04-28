import copy
from urllib.parse import quote

from fhirpathpy.models import models
from fhirpy.base.exceptions import OperationOutcome
from fhirpy.base.utils import get_by_path
from fpml import resolve_template
from funcy.seqs import first
from funcy.strings import re_all
from funcy.types import is_list, is_mapping

from app.cached_fhirpath import fhirpath
from app.sdc.getters import get_source_queries
from app.sdc.typings import Expression, LaunchContext

from .exception import ConstraintCheckOperationOutcome

r4 = models["r4"]


def get_type(item, data):
    type = item["type"]
    if type == "choice" or type == "open-choice":
        option_type = [
            key.removeprefix("value")
            for key in get_by_path(item, ["answerOption", 0], {}).keys()
            if key.startswith("value")
        ]
        if option_type:
            type = next(iter(option_type))
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
    elif type == "date":
        type = "date"
    elif type == "dateTime":
        type = "dateTime"
    elif type == "time":
        type = "time"
    elif type == "boolean":
        type = "boolean"
    elif type == "attachment":
        type = "Attachment"
    elif type == "display":
        type = "string"
    elif type == "reference":
        type = "Reference"
    elif type == "quantity":
        type = "Quantity"
    elif type == "url":
        type = "uri"  # FHIR uses valueUri for url item type
    # TODO: deprecate email and phone
    elif type == "email":
        type = "string"
    elif type == "phone":
        type = "string"

    return type


def make_value_key(type_: str) -> str:
    return f"value{type_[0].upper()}{type_[1:]}"


def normalize_answer_value(type_: str, value):
    # Resource (that contains resourceType and id) should be converted to Reference
    # It's according to the spec of $populate
    if (
        type_ == "Reference"
        and isinstance(value, dict)
        and "resourceType" in value
        and "id" in value
    ):
        return {"reference": f"{value['resourceType']}/{value['id']}"}
    return value


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
            return resolve_string_template({}, value, variables)
        else:
            return value

    return _update_link_id_or_question


def prepare_link_ids(questionnaire, variables):
    return walk_dict(questionnaire, update_link_id_or_question(variables))


def prepare_bundle(raw_bundle, env):
    return walk_dict(
        raw_bundle,
        lambda value, _k: resolve_string_template({}, value, env, encode_result=True),
    )


def resolve_string_template(
    context, expr: str, env, *, encode_result=False, return_null_if_unresolved=False
):
    if not isinstance(expr, str):
        return expr
    exprs = re_all(r"(?P<var>{{[\S\s]+?}})", expr)
    vs = {}
    for exp in exprs:
        data = fhirpath(context, exp["var"][2:-2], env)
        if len(data) > 0:
            # NOTE: http://build.fhir.org/ig/HL7/sdc/expressions.html#x-fhir-query-enhancements
            # If the expression resolves to a collection of more than one value,
            # the substitution will be a list of comma-separated values (i.e. behaving as 'or').
            search_str = ",".join([str(item) for item in data])
            vs[exp["var"]] = quote(search_str) if encode_result else search_str
        else:
            if return_null_if_unresolved:
                return None
            vs[exp["var"]] = ""
    res = expr
    for k, v in vs.items():
        res = res.replace(k, v)

    return res


def prepare_assemble_variables(item):
    # Assemble supports only fhirpath expressions
    variables = {}
    for var in item.get("variable", []):
        if var["language"] == "text/fhirpath":
            variables[var["name"]] = fhirpath({}, var["expression"])
    return variables


def parameter_to_env(resource, is_fhir: bool = True):
    env = {}
    for param in resource["parameter"]:
        if param["name"] == "context":
            n = [p for p in param['part'] if p['name'] == 'name'][0]['valueString']
            c = [p for p in param['part'] if p['name'] == 'content'][0]
            get = [k for k in c.keys() if k != 'name'][0]
            env[n] = c[get]
        elif "resource" in param:
            env[param["name"]] = param["resource"]
        else:
            value = parse_parameter_value(param, is_fhir)
            if value:
                env[param["name"]] = value
    # Mapping parameters to fhir resource names
    questionnaire = env.get("questionnaire")
    if questionnaire:
        env["Questionnaire"] = questionnaire
    questionnaire_response = env.get("questionnaire_response")
    if questionnaire_response:
        env["QuestionnaireResponse"] = questionnaire_response
    return env


def parse_parameter_value(parameter, is_fhir: bool):
    if is_fhir:
        _name_key, value_key = parameter.keys()
        return parameter[value_key]
    else:
        value = parameter["value"]
        polimorphic_key = first(value.keys())
        return value[polimorphic_key] if polimorphic_key else None


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
    contained_new = {item["id"]: item for item in fce_questionnaire.get("contained", [])}
    contained = {**contained_compat, **contained_new}

    # TODO: get rid of FCE format completely
    source_queries_fce = fce_questionnaire.get("sourceQueries", {})
    source_queries_fhir = get_source_queries(fce_questionnaire.get("extension", []))
    source_queries = [*source_queries_fce, *source_queries_fhir]

    if isinstance(source_queries, dict):
        source_queries = [source_queries]

    for source_query in source_queries:
        # FHIR reference contains #, while FCE localRef does not
        ref = (
            source_query["reference"].removeprefix("#")
            if "reference" in source_query
            else source_query.get("localRef")
        )
        if ref:
            # TODO: raise a clear error
            raw_bundle = contained[ref]
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


def validate_context(context_definition: list[LaunchContext], env):
    all_vars = env.keys()
    errors = []
    for item in context_definition:
        if isinstance(item["name"], str):
            name = item["name"]
        else:
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


async def resolve_expression(client, context, expression: Expression, env, path: str):
    try:
        if expression["language"] == "text/fhirpath":
            return fhirpath(context, expression["expression"], env)
        elif expression["language"] == "application/x-fhir-query":
            url = resolve_string_template(
                context,
                expression["expression"],
                env,
                encode_result=True,
                return_null_if_unresolved=True,
            )
            if url is None:
                return None
            return await client.execute(
                url,
                method="GET",
            )
    except Exception as e:
        raise OperationOutcome(
            f'Error resolving expression at {path}: "{expression["expression"]}" - {str(e)}'
        )

    raise OperationOutcome(f"Unsupported expression language: {expression['language']} at {path}")
