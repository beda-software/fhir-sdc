from .utils import load_source_queries


async def get_questionnaire_context(client, env):
    questionnaire = env["Questionnaire"]
    await load_source_queries(client, questionnaire, env)
    return env
