from functools import lru_cache

from fhirpathpy import compile
from fhirpathpy.models import models


@lru_cache(maxsize=2**14)
def cached_compile(expression, model=None):
    m = models.get(model)
    return compile(expression, m)


def fhirpath(context, expression, env=None, model=None):
    compiled_expression = cached_compile(expression, model)
    return compiled_expression(context, env or {})
