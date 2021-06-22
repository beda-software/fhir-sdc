from aiohttp import web

from app.sdk import sdk

from ..operations.constraint_check import constraint_check
from .exception import ConstraintCheckOperationOutcome
from .utils import parameter_to_env, validate_context


@sdk.operation(["POST"], ["Questionnaire", "$extract"])
async def extract_questionnaire(operation, request):
    resource = request["resource"]

    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = sdk.client.resource("QuestionnaireResponse", **request["resource"])
        questionnaire = (
            await sdk.client.resources("Questionnaire")
            .search(id=questionnaire_response["questionnaire"])
            .get()
        )
        context = {"Questionnaire": questionnaire, "QuestionnaireResponse": questionnaire_response}
        return await extract(questionnaire, context)

    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request["resource"])

        questionnaire_data = env.get("Questionnaire")
        if not questionnaire_data:
            raise ConstraintCheckOperationOutcome(
                [
                    {
                        "severity": "error",
                        "key": "missing-parameter",
                        "human": "Questionnaire parameter is required",
                    }
                ]
            )

        questionnaire = sdk.client.resource("Questionnaire", **questionnaire_data)

        questionnaire_response_data = env.get("questionnaire_response") or env.get(
            "QuestionnaireResponse"
        )
        if not questionnaire_response_data:
            raise ConstraintCheckOperationOutcome(
                [
                    {
                        "severity": "error",
                        "key": "missing-parameter",
                        "human": "QuestionnaireResponse parameter is required",
                    }
                ]
            )

        questionnaire_response = sdk.client.resource(
            "QuestionnaireResponse", **questionnaire_response_data
        )
        if "launchContext" in questionnaire:
            validate_context(questionnaire["launchContext"], env)
        return await extract(
            questionnaire,
            {
                "QuestionnaireResponse": questionnaire_response,
                "Questionnaire": questionnaire,
                **env,
            },
        )

    raise ConstraintCheckOperationOutcome(
        [
            {
                "severity": "error",
                "key": "missing-parameter",
                "human": "Either `QuestionnaireResponse` resource or Parameters containing "
                "QuestionnaireResponse are required",
            }
        ]
    )


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
async def extract_questionnaire_instance(operation, request):
    questionnaire = (
        await sdk.client.resources("Questionnaire").search(id=request["route-params"]["id"]).get()
    )

    resource = request["resource"]

    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = sdk.client.resource("QuestionnaireResponse", **request["resource"])
        context = {"Questionnaire": questionnaire, "QuestionnaireResponse": questionnaire_response}

        return await extract(questionnaire, context)

    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request["resource"])

        questionnaire_response_data = env.get("QuestionnaireResponse")
        if not questionnaire_response_data:
            raise ConstraintCheckOperationOutcome(
                [
                    {
                        "severity": "error",
                        "key": "missing-parameter",
                        "human": "`QuestionnaireResponse` parameter is required",
                    }
                ]
            )

        questionnaire_response = sdk.client.resource(
            "QuestionnaireResponse", **questionnaire_response_data
        )
        if "launchContext" in questionnaire:
            validate_context(questionnaire["launchContext"], env)
        return await extract(
            questionnaire,
            {
                "QuestionnaireResponse": questionnaire_response,
                "Questionnaire": questionnaire,
                **env,
            },
        )

    raise ConstraintCheckOperationOutcome(
        [
            {
                "severity": "error",
                "key": "missing-parameter",
                "human": "Either `QuestionnaireResponse` resource or Parameters containing "
                "QuestionnaireResponse are required",
            }
        ]
    )


async def extract(questionnaire, context):
    await constraint_check(context)

    resp = []
    for mapper in questionnaire.get("mapping", []):
        resp.append(
            await sdk.client.resource("Mapping", id=mapper.id).execute("$apply", data=context)
        )

    return web.json_response(resp)
