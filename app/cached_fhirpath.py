from functools import lru_cache

from fhirpathpy import compile
from fhirpathpy.models import models

FHIRPATH_CACHE_SIZE = 2**14


def answers(inputs, link_id):
    return fhirpath(
        inputs,
        "repeat(item).where(linkId=%FPMLLinkId).answer.value",
        {"FPMLLinkId": link_id},
        "r4",
    )


# Baked into every compilation, because lru_cache accepts only hashable arguments
options = {
    "userInvocationTable": {
        "answers": {
            "fn": answers,
            "arity": {0: [], 1: ["String"]},
        },
    },
}


@lru_cache(maxsize=FHIRPATH_CACHE_SIZE)
def cached_compile(expression, model=None):
    m = models.get(model)
    return compile(expression, m, options)


def fhirpath(context, expression, env=None, model=None):
    compiled_expression = cached_compile(expression, model)
    return compiled_expression(context, env or {})
