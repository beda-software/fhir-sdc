from aiohttp import ClientSession, web

from app.sdk import sdk

from ..operations.constraint_check import constraint_check
from .exception import ConstraintCheckOperationOutcome
from .utils import get_user_sdk_client, parameter_to_env, validate_context


@sdk.operation(["POST"], ["Questionnaire", "$extract"])
async def extract_questionnaire(_operation, request):
    resource = request["resource"]
    client = request["app"]["client"]
    jute_service = request["app"]["settings"].JUTE_SERVICE

    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = client.resource("QuestionnaireResponse", **request["resource"])
        questionnaire = (
            await client.resources("Questionnaire")
            .search(id=questionnaire_response["questionnaire"])
            .get()
        )
        context = {"Questionnaire": questionnaire, "QuestionnaireResponse": questionnaire_response}
        client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)
        await constraint_check(client, context)
        return await extract(client, questionnaire, context, jute_service)

    if resource["resourceType"] == "Parameters":
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

        questionnaire = client.resource("Questionnaire", **questionnaire_data)

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

        questionnaire_response = client.resource(
            "QuestionnaireResponse", **questionnaire_response_data
        )
        if "launchContext" in questionnaire:
            validate_context(questionnaire["launchContext"], env)
        client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)
        context = {
            "QuestionnaireResponse": questionnaire_response,
            "Questionnaire": questionnaire,
            **env,
        }
        await constraint_check(client, context)
        return await extract(client, questionnaire, context, jute_service)

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
async def extract_questionnaire_instance(_operation, request):
    client = request["app"]["client"]
    jute_service = request["app"]["settings"].JUTE_SERVICE
    questionnaire = (
        await client.resources("Questionnaire").search(id=request["route-params"]["id"]).get()
    )

    resource = request["resource"]
    client = client if questionnaire.get("runOnBehalfOfRoot") else get_user_sdk_client(request)

    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = client.resource("QuestionnaireResponse", **request["resource"])
        context = {"Questionnaire": questionnaire, "QuestionnaireResponse": questionnaire_response}
        await constraint_check(client, context)
        return await extract(client, questionnaire, context, jute_service)

    if resource["resourceType"] == "Parameters":
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

        questionnaire_response = client.resource(
            "QuestionnaireResponse", **questionnaire_response_data
        )
        if "launchContext" in questionnaire:
            validate_context(questionnaire["launchContext"], env)
        context = {
            "QuestionnaireResponse": questionnaire_response,
            "Questionnaire": questionnaire,
            **env,
        }
        await constraint_check(client, context)
        return await extract(client, questionnaire, context, jute_service)

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


async def extract(client, questionnaire, context, jute_service):
    resp = []
    if jute_service == "aidbox":
        for mapper in questionnaire.get("mapping", []):
            resp.append(
                await client.resource("Mapping", id=mapper.id).execute("$apply", data=context)
            )
    else:
        for mr in questionnaire.get("mapping", []):
            mapping = client.resource("Mapping", id=mr.id)
            await mapping.refresh()
            async with ClientSession() as session:
                async with session.post(
                    jute_service,
                    json={
                        "template": mapping["body"],
                        "context": context,
                    },
                ) as result:
                    bundle = await result.json()
                    resp.append(await client.execute("/", data=bundle))
    return web.json_response(resp)
