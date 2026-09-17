"""What a test writes: an answer, a set of answers, and the launch context to populate with."""

from collections.abc import Mapping, Sequence

import fhirpy_types_r4b as r4b

answer = r4b.QuestionnaireResponseItemAnswer
Answers = Mapping[str, "Sequence[r4b.QuestionnaireResponseItemAnswer] | Sequence[Answers]"]
LaunchContextValue = r4b.AnyResource | r4b.Reference
LaunchContext = dict[str, "LaunchContextValue | list[LaunchContextValue]"]


def launch_context(context: LaunchContext) -> r4b.Parameters:
    """One `context` parameter per resource — fhir-sdc keeps only the last of a repeated name."""
    return r4b.Parameters(
        parameter=[
            build_context_parameter(name, value)
            for name, values in context.items()
            for value in (values if isinstance(values, list) else [values])
        ]
    )


def build_context_parameter(name: str, value: LaunchContextValue) -> r4b.ParametersParameter:
    content = (
        r4b.ParametersParameter(name="content", valueReference=value)
        if isinstance(value, r4b.Reference)
        else r4b.ParametersParameter(name="content", resource=value)
    )
    return r4b.ParametersParameter(
        name="context",
        part=[r4b.ParametersParameter(name="name", valueString=name), content],
    )
