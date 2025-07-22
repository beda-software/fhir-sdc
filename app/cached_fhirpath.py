from functools import lru_cache

from fhirpathpy import compile


@lru_cache(maxsize=2**14)
def cached_compile(expression):
    return compile(expression)


def fhirpath(context, expression, env=None, model=None):
    compiled_expression = cached_compile(expression)
    return compiled_expression(context, env or {}, model)
