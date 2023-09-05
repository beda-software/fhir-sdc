from aiohttp import ClientSession

from .constraint_check import constraint_check
from .exception import ConstraintCheckOperationOutcome
from .utils import parameter_to_env, validate_context


async def extract_questionnaire_instance(
    aidbox_client, extract_client, questionnaire, resource, extract_services
):
    # TODO move to Aidbox
    if resource["resourceType"] == "QuestionnaireResponse":
        questionnaire_response = extract_client.resource("QuestionnaireResponse", **resource)
        context = {"Questionnaire": questionnaire, "QuestionnaireResponse": questionnaire_response}
        mappings = [
            await aidbox_client.resources("Mapping").search(_id=m["id"]).get()
            for m in questionnaire.get("mapping", [])
        ]
        await constraint_check(extract_client, context)
        return await extract(extract_client, mappings, context, extract_services)

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

        questionnaire_response = extract_client.resource(
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
            await aidbox_client.resources("Mapping").search(_id=m["id"]).get()
            for m in questionnaire.get("mapping", [])
        ]
        await constraint_check(extract_client, context)
        return await extract(extract_client, mappings, context, extract_services)

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


async def external_service_extraction(client, service, template, context):
    async with ClientSession() as session:
        async with session.post(
            service,
            json={
                "template": template,
                "context": context,
            },
        ) as result:
            bundle = await result.json()
            return await client.execute("/", data=bundle)


async def extract(client, mappings, context, extract_services):
    """
    mappings could be a list of Aidbox Mapping resources
    or plain jute templates
    """
    resp = []

    for mapper in mappings:
        if "resourceType" in mapper and "body" in mapper:
            # It is custome mapper resource
            mapper_type = mapper.get("type", "JUTE")
            if mapper_type == "JUTE" and extract_services["JUTE"] == "aidbox":
                # Aidbox native extraction
                resp.append(
                    await client.resource("Mapping", id=mapper.id).execute("$apply", data=context)
                )
            else:
                # Use 3rd party service FHIRPathMapping or JUTE
                resp.append(
                    await external_service_extraction(
                        client, extract_services[mapper_type], mapper["body"], context
                    )
                )
        else:
            # legacy extraction
            resp.append(
                await external_service_extraction(client, extract_services["JUTE"], mapper, context)
            )
    return resp
