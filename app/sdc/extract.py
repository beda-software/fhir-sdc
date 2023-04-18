from aiohttp import ClientSession

from .constraint_check import constraint_check
from .exception import ConstraintCheckOperationOutcome
from .utils import parameter_to_env, validate_context


async def extract_questionnaire(client, resource, jute_service):
    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = client.resource("QuestionnaireResponse", **resource)
        questionnaire = (
            await client.resources("Questionnaire")
            .search(id=questionnaire_response["questionnaire"])
            .get()
        )
        context = {"Questionnaire": questionnaire, "QuestionnaireResponse": questionnaire_response}
        await constraint_check(client, context)
        return await extract(client, questionnaire, context, jute_service)

    if resource["resourceType"] == "Parameters":
        env = parameter_to_env(resource)

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


async def extract_questionnaire_instance(client, questionnaire, resource, jute_service):
    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = client.resource("QuestionnaireResponse", **resource)
        context = {"Questionnaire": questionnaire, "QuestionnaireResponse": questionnaire_response}
        mappings = [
            await client.resources("Mapping").search(_id=m["id"]).get()
            for m in questionnaire.get("mapping", [])
        ]
        await constraint_check(client, context)
        return await extract(client, mappings, context, jute_service)

    if resource["resourceType"] == "Parameters":
        env = parameter_to_env(resource)

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
        mappings = [
            await client.resources("Mapping").search(_id=m["id"]).get()
            for m in questionnaire.get("mapping", [])
        ]
        await constraint_check(client, context)
        return await extract(client, mappings, context, jute_service)

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


async def extract(client, mappings, context, jute_service):
    resp = []
    if jute_service == "aidbox":
        for mapper in mappings:
            resp.append(
                await client.resource("Mapping", id=mapper.id).execute("$apply", data=context)
            )
    else:
        for mapper in mappings:
            async with ClientSession() as session:
                async with session.post(
                    jute_service,
                    json={
                        "template": mapper,
                        "context": context,
                    },
                ) as result:
                    bundle = await result.json()
                    resp.append(await client.execute("/", data=bundle))
    return resp
