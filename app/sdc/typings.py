from typing import TypedDict


class Expression(TypedDict, total=False):
    name: str
    language: str
    expression: str


class Coding(TypedDict, total=False):
    code: str
    system: str | None
    display: str | None


class LaunchContext(TypedDict, total=False):
    name: Coding
    type: list[str]


class Reference(TypedDict, total=False):
    reference: str


class ItemConstraint(TypedDict, total=False):
    key: str
    severity: str
    human: str
    expression: str
