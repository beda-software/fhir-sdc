from app.cached_fhirpath import fhirpath
from .exception import ConstraintCheckOperationOutcome
from .getters import get_item_constraints, get_launch_context
from .utils import load_source_queries, validate_context


async def constraint_check(client, questionnaire, env, *, legacy_behavior=False):
    launch_context = get_launch_context(questionnaire.get("extension", []))
    if launch_context:
        validate_context(launch_context, env)
    await load_source_queries(client, questionnaire, env)
    errors = []
    _constraint_check_for_item(errors, questionnaire, env, legacy_behavior=legacy_behavior)
    if len(errors) > 0:
        raise ConstraintCheckOperationOutcome(errors)
    return env["QuestionnaireResponse"]


def _constraint_check_for_item(errors, questionnaire_item, env, *, legacy_behavior=False):
    for constraint in get_item_constraints(questionnaire_item.get("extension", [])):
        expression = constraint["expression"]
        result = fhirpath({}, expression, env)

        if result == [True if legacy_behavior else False]:
            errors.append(constraint)

    for item in questionnaire_item.get("item", []):
        _constraint_check_for_item(errors, item, env, legacy_behavior=legacy_behavior)
