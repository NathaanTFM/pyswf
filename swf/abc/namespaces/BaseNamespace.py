from __future__ import annotations
from typing import Any, ClassVar

class BaseNamespace:
    kind: ClassVar[int]
    name: str | None

    def __init__(self, name: str | None) -> None:
        self.name = name


    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__.__name__, self.name)


    def __eq__(self, other: Any) -> bool:
        return type(self) == type(other) and self.name == other.name


    def __hash__(self) -> int:
        return hash((self.kind, self.name))