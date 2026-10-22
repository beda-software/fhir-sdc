from typing import Any

from fhirpy import AsyncFHIRClient

from .getters import get_launch_context
from .utils import build_fhirpath_env, load_source_queries, validate_context


async def load_questionnaire_context(
    client: AsyncFHIRClient,
    questionnaire: dict,
    questionnaire_response: dict | None,
    variables: dict[str, Any],
) -> dict:
    """The FHIRPath env with the launch context checked and the source queries loaded."""
    env = build_fhirpath_env(questionnaire, questionnaire_response, variables)
    launch_context = get_launch_context(questionnaire.get("extension", []))
    if launch_context:
        validate_context(launch_context, env)
    await load_source_queries(client, questionnaire, env)
    return env
