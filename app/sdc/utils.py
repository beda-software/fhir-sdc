from urllib.parse import quote

from fhirpathpy import evaluate as fhirpath
from fhirpy.base.utils import get_by_path
from funcy.seqs import first
from funcy.strings import re_all
from funcy.types import is_list, is_mapping

from .exception import ConstraintCheckOperationOutcome


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

    return type


def walk_dict(d, transform):
    for k, v in d.items():
        if is_list(v):
            d[k] = [walk_dict(vi, transform) for vi in v]
        elif is_mapping(v):
            d[k] = walk_dict(v, transform)
        else:
            d[k] = transform(v, k)
    return d


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
            value = param["value"]
            polimorphic_key = first(value.keys())
            if polimorphic_key:
                env[param["name"]] = value[polimorphic_key]
    # Mapping parameters to fhir resource names
    questionnaire = env.get("questionnaire")
    if questionnaire:
        env["Questionnaire"] = questionnaire
    questionnaire_response = env.get("questionnaire_response")
    if questionnaire_response:
        env["QuestionnaireResponse"] = questionnaire_response
    return env


async def load_source_queries(client, questionnaire, env):
    contained = {
        f"{item['resourceType']}#{item['id']}": item for item in questionnaire.get("contained", [])
    }

    source_queries = questionnaire.get("sourceQueries", {})

    if isinstance(source_queries, dict):
        source_queries = [source_queries]

    for source_query in source_queries:
        if "localRef" in source_query:
            raw_bundle = contained[source_query["localRef"]]
            if raw_bundle:
                bundle = prepare_bundle(raw_bundle, env)
                env[bundle["id"]] = await client.execute("/", data=bundle)


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
