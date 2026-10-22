from typing import Any

from fhirpy import AsyncFHIRClient

from app.cached_fhirpath import fhirpath

from .context import load_questionnaire_context
from .exception import ConstraintCheckOperationOutcome
from .getters import get_item_constraints


async def constraint_check(
    client: AsyncFHIRClient,
    questionnaire: dict,
    questionnaire_response: dict,
    variables: dict[str, Any],
) -> dict:
    env = await load_questionnaire_context(client, questionnaire, questionnaire_response, variables)
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
