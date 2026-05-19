import copy
from typing import Any
from urllib.parse import quote

from fhirpathpy.models import models
from fhirpy import AsyncFHIRClient
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

# NOTE: it's outside from spec
EXTERNAL_FHIR_BASE_URL_PARAM_KEY = "externalFhirBaseUrl"


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
    from app.sdc.getters import get_variable

    variables = {}
    for var in get_variable(item.get("extension", [])):
        if var and var.get("language") == "text/fhirpath":
            variables[var["name"]] = fhirpath({}, var["expression"])
    return variables


def is_sdc_api(parameters: dict | None) -> bool:
    """True when Parameters use SDC `$populate` input shape (`context` and/or `subject`)."""
    if not parameters or parameters.get("resourceType") != "Parameters":
        return False
    return any(p.get("name") in ("context", "subject") for p in parameters.get("parameter", []))


async def parameter_to_env(client: AsyncFHIRClient, resource) -> dict[str, Any]:
    # TODO: add support for repeating values (with same name)
    env: dict[str, Any] = {}
    for param in resource["parameter"]:
        if param["name"] == "context":
            parts = param["part"]
            name = next(p for p in parts if p["name"] == "name")["valueString"]
            value = next(p for p in parts if p["name"] == "content")
            if "resource" in value:
                env[name] = value["resource"]
            else:
                env[name] = await client.reference(
                    reference=value["valueReference"]["reference"]
                ).to_resource()
        elif "resource" in param:
            env[param["name"]] = param["resource"]
        else:
            value, kind = parse_parameter_value(param)
            if value:
                if param["name"] == "subject" and kind == "Reference":
                    env[param["name"]] = await client.reference(
                        reference=value["reference"]
                    ).to_resource()
                else:
                    env[param["name"]] = value
    # Mapping parameters to fhir resource names
    questionnaire = env.get("questionnaire")
    if questionnaire:
        env["Questionnaire"] = questionnaire
    questionnaire_response = env.get("questionnaire_response")
    if questionnaire_response:
        env["QuestionnaireResponse"] = questionnaire_response
    return env


def parse_parameter_value(parameter) -> tuple[Any, str]:
    _name_key, value_key = parameter.keys()
    return parameter[value_key], value_key.removeprefix("value")


def get_external_fhir_base_url_from_resource(resource: dict | None):
    if not resource or resource.get("resourceType") != "Parameters":
        return None
    for param in resource.get("parameter", []):
        if param.get("name") != EXTERNAL_FHIR_BASE_URL_PARAM_KEY:
            continue
        if "resource" in param:
            continue
        value, _key = parse_parameter_value(param)
        return value or None
    return None


async def load_source_queries(client, questionnaire, env):
    contained = {item["id"]: item for item in questionnaire.get("contained", [])}
    source_queries = get_source_queries(questionnaire.get("extension", []))

    for source_query in source_queries:
        ref = source_query.get("reference", "").removeprefix("#")
        if ref:
            raw_bundle = contained.get(ref)
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
        name = (item.get("name") or {}).get("code", "")
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
