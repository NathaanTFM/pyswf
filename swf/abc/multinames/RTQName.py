from __future__ import annotations
from typing import Any
from swf.abc.multinames.BaseMultiname import BaseMultiname


class RTQName(BaseMultiname):
    kind = 0x0F

    name: str | None

    def __init__(self, name: str | None) -> None:
        self.name = name


    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__.__name__, self.name)


    def __eq__(self, other: Any) -> bool:
        return type(other) == RTQName and self.name == other.name


    def __hash__(self) -> int:
        return hash((self.kind, self.name))