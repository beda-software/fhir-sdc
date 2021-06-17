from aiohttp import web
from fhirpathpy import evaluate as fhirpath

from app.sdk import sdk

from .exception import ConstraintCheckOperationOutcome
from .utils import load_source_queries, parameter_to_env, validate_context


@sdk.operation(["POST"], ["QuestionnaireResponse", "$constraint-check"])
async def constraint_check_operation(operation, request):
    env = parameter_to_env(request["resource"])
    questionnaire = env["Questionnaire"]
    if "launchContext" in questionnaire:
        validate_context(questionnaire["launchContext"], env)
    return web.json_response(await constraint_check(env))


async def constraint_check(env):
    questionnaire = env["Questionnaire"]
    questionnaire_response = env["QuestionnaireResponse"]
    await load_source_queries(sdk, questionnaire, env)
    errors = []
    await constraint_check_for_item(errors, questionnaire, env)
    if len(errors) > 0:
        raise ConstraintCheckOperationOutcome(errors)
    return questionnaire_response


async def constraint_check_for_item(errors, questionnaire_item, env):
    for constraint in questionnaire_item.get("constraint", []):
        expression = constraint["expression"]["expression"]
        result = fhirpath({}, expression, env)
        import logging

        logging.debug("expression %s", expression)
        logging.debug("result %s", result)
        logging.debug("env %s", env)

        if result == [True]:
            # TODO: calculate error location path
            errors.append(constraint)

    for item in questionnaire_item.get("item", []):
        await constraint_check_for_item(errors, item, env)
