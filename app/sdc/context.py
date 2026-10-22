from fhirpy import AsyncFHIRClient

from .utils import build_fhirpath_env, load_source_queries


async def get_questionnaire_context(
    client: AsyncFHIRClient,
    questionnaire: dict,
    questionnaire_response: dict | None,
    variables: dict,
) -> dict:
    env = build_fhirpath_env(questionnaire, questionnaire_response, variables)
    await load_source_queries(client, questionnaire, env)
    return env
