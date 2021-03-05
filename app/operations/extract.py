from aiohttp import web

from app.sdk import sdk

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
        return await extract(questionnaire, questionnaire_response)

    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request["resource"])

        questionnaire_data = env.get("questionnaire") or env.get("Questionnaire")
        if not questionnaire_data:
            # TODO: return OperationOutcome
            return web.json_response(
                {
                    "error": "bad_request",
                    "error_description": "`Questionnaire` parameter is required",
                },
                status=422,
            )

        questionnaire = sdk.client.resource("Questionnaire", **questionnaire_data)

        questionnaire_response_data = env.get("questionnaire_response") or env.get(
            "QuestionnaireResponse"
        )
        if not questionnaire_response_data:
            # TODO: return OperationOutcome
            return web.json_response(
                {
                    "error": "bad_request",
                    "error_description": "`QuestionnaireResponse` parameter is required",
                },
                status=422,
            )

        questionnaire_response = sdk.client.resource(
            "QuestionnaireResponse", **questionnaire_response_data
        )
        if "launchContext" in questionnaire:
            validate_context(questionnaire["launchContext"], env)
        return await extract(
            questionnaire, {"QuestionnaireResponse": questionnaire_response, **env}
        )

    # TODO: return OperationOutcome
    return web.json_response(
        {
            "error": "bad_request",
            "error_description": "Either `QuestionnaireResponse` resource or Parameters containing "
            "QuestionnaireResponse and Questionnaire are required",
        },
        status=422,
    )


@sdk.operation(["POST"], ["Questionnaire", {"name": "id"}, "$extract"])
async def extract_questionnaire_instance(operation, request):
    questionnaire = (
        await sdk.client.resources("Questionnaire").search(id=request["route-params"]["id"]).get()
    )

    resource = request["resource"]

    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = sdk.client.resource("QuestionnaireResponse", **request["resource"])
        return await extract(questionnaire, questionnaire_response)

    elif resource["resourceType"] == "Parameters":
        env = parameter_to_env(request["resource"])

        questionnaire_response_data = env.get("questionnaire_response") or env.get(
            "QuestionnaireResponse"
        )
        if not questionnaire_response_data:
            return web.json_response(
                {
                    "error": "bad_request",
                    "error_description": "`QuestionnaireResponse` parameter is required",
                },
                status=422,
            )

        questionnaire_response = sdk.client.resource(
            "QuestionnaireResponse", **questionnaire_response_data
        )
        if "launchContext" in questionnaire:
            validate_context(questionnaire["launchContext"], env)
        return await extract(
            questionnaire, {"QuestionnaireResponse": questionnaire_response, **env}
        )

    return web.json_response(
        {
            "error": "bad_request",
            "error_description": "Either `QuestionnaireResponse` resource or Parameters containing "
            "QuestionnaireResponse are required",
        },
        status=422,
    )


async def extract(questionnaire, context):
    resp = []
    for mapper in questionnaire.get("mapping", []):
        resp.append(
            await sdk.client.resource("Mapping", id=mapper.id).execute("$apply", data=context)
        )

    return web.json_response(resp)
