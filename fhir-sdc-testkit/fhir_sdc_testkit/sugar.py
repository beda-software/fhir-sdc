"""What a test writes: an answer, a set of answers, and the launch context to populate with."""

from collections.abc import Mapping, Sequence

import fhirpy_types_r4b as r4b

answer = r4b.QuestionnaireResponseItemAnswer
Answers = Mapping[str, "Sequence[r4b.QuestionnaireResponseItemAnswer] | Sequence[Answers]"]
LaunchContextValue = r4b.AnyResource | r4b.Reference
LaunchContext = dict[str, "LaunchContextValue | list[LaunchContextValue]"]


def launch_context(
    context: LaunchContext, *, subject: r4b.Reference | None = None
) -> r4b.Parameters:
    """SDC `$populate` input: one `context` parameter per name, with a `content` part per value."""
    parameters = [
        build_context_parameter(name, values if isinstance(values, list) else [values])
        for name, values in context.items()
    ]
    if subject is not None:
        parameters.append(r4b.ParametersParameter(name="subject", valueReference=subject))
    return r4b.Parameters(parameter=parameters)


def build_context_parameter(name: str, values: list[LaunchContextValue]) -> r4b.ParametersParameter:
    if not values:
        raise ValueError(f"Launch context {name!r} needs at least one value")

    return r4b.ParametersParameter(
        name="context",
        part=[
            r4b.ParametersParameter(name="name", valueString=name),
            *(build_content_part(value) for value in values),
        ],
    )


def build_content_part(value: LaunchContextValue) -> r4b.ParametersParameter:
    if isinstance(value, r4b.Reference):
        return r4b.ParametersParameter(name="content", valueReference=value)

    return r4b.ParametersParameter(name="content", resource=value)
