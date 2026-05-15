from fhirpy_types_r4b import Questionnaire

from .utils import load_source_queries


async def get_questionnaire_context(client, questionnaire: Questionnaire, env):
    await load_source_queries(client, questionnaire, env)
    return env
