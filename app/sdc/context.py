from .utils import load_source_queries


async def get_questionnaire_context(client, questionnaire, env):
    await load_source_queries(client, questionnaire, env)
    return env
