from fhirpy import AsyncFHIRClient

from app.cached_fhirpath import fhirpath

from .exception import ConstraintCheckOperationOutcome
from .getters import get_item_constraints, get_launch_context
from .utils import build_fhirpath_env, load_source_queries, validate_context


async def constraint_check(
    client: AsyncFHIRClient, questionnaire: dict, questionnaire_response: dict, variables: dict
) -> dict:
    env = build_fhirpath_env(questionnaire, questionnaire_response, variables)
    launch_context = get_launch_context(questionnaire.get("extension", []))
    if launch_context:
        validate_context(launch_context, env)
    await load_source_queries(client, questionnaire, env)
    errors = []
    _constraint_check_for_item(errors, questionnaire, env)
    if len(errors) > 0:
        raise ConstraintCheckOperationOutcome(errors)
    return questionnaire_response


def _constraint_check_for_item(errors, questionnaire_item, env):
    for constraint in get_item_constraints(questionnaire_item.get("extension", [])):
        expression = constraint["expression"]
        result = fhirpath({}, expression, env)

        if result == [False]:
            # TODO: calculate error location path
            errors.append(constraint)

    for item in questionnaire_item.get("item", []):
        _constraint_check_for_item(errors, item, env)
