from typing import Optional, TypedDict


class Expression(TypedDict, total=False):
    name: str
    language: str
    expression: str


class Coding(TypedDict, total=False):
    code: str
    system: Optional[str]
    display: Optional[str]


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
