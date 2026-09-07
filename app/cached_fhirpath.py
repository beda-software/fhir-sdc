from functools import lru_cache

from fhirpathpy import compile
from fhirpathpy.models import models
from fpml import ExpressionCache

FHIRPATH_CACHE_SIZE = 2**14
FPML_CACHE_SIZE = 2048

# Separate from cached_compile, which serves several models: fpml keys entries by expression alone
fpml_expression_cache = ExpressionCache(max_size=FPML_CACHE_SIZE)


@lru_cache(maxsize=FHIRPATH_CACHE_SIZE)
def cached_compile(expression, model=None):
    m = models.get(model)
    return compile(expression, m)


def fhirpath(context, expression, env=None, model=None):
    compiled_expression = cached_compile(expression, model)
    return compiled_expression(context, env or {})
