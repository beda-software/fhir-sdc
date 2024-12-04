from .utils import load_source_queries


async def get_questionnaire_context(client, fce_questionnaire, env):
    await load_source_queries(client, fce_questionnaire, env)
    return env
