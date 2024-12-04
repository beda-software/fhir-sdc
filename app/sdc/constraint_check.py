from fhirpathpy import evaluate as fhirpath

from .exception import ConstraintCheckOperationOutcome
from .utils import load_source_queries, validate_context


async def constraint_check(client, fce_questionnaire, env):
    if "launchContext" in fce_questionnaire:
        validate_context(fce_questionnaire["launchContext"], env)
    await load_source_queries(client, fce_questionnaire, env)
    errors = []
    _constraint_check_for_item(errors, fce_questionnaire, env)
    if len(errors) > 0:
        raise ConstraintCheckOperationOutcome(errors)
    return env["QuestionnaireResponse"]


def _constraint_check_for_item(errors, questionnaire_item, env):
    for constraint in questionnaire_item.get("itemConstraint", []):
        expression = constraint["expression"]
        result = fhirpath({}, expression, env)

        if result == [True]:
            # TODO: calculate error location path
            errors.append(constraint)

    for item in questionnaire_item.get("item", []):
        _constraint_check_for_item(errors, item, env)
