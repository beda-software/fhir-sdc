from fhirpathpy import evaluate as fhirpath

from .exception import ConstraintCheckOperationOutcome
from .utils import load_source_queries, validate_context


async def constraint_check(client, env):
    questionnaire = env["Questionnaire"]
    questionnaire_response = env["QuestionnaireResponse"]
    if "launchContext" in questionnaire:
        validate_context(questionnaire["launchContext"], env)
    await load_source_queries(client, questionnaire, env)
    errors = []
    constraint_check_for_item(errors, questionnaire, env)
    if len(errors) > 0:
        raise ConstraintCheckOperationOutcome(errors)
    return questionnaire_response


def constraint_check_for_item(errors, questionnaire_item, env):
    for constraint in questionnaire_item.get("itemConstraint", []):
        expression = constraint["expression"]
        result = fhirpath({}, expression, env)

        if result == [True]:
            # TODO: calculate error location path
            errors.append(constraint)

    for item in questionnaire_item.get("item", []):
        constraint_check_for_item(errors, item, env)
