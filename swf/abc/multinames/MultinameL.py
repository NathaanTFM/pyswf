from __future__ import annotations
from typing import Any
from swf.abc.multinames.BaseMultiname import BaseMultiname
from swf.abc.namespaces.BaseNamespace import BaseNamespace


class MultinameL(BaseMultiname):
    kind = 0x1B

    nsSet: list[BaseNamespace]

    def __init__(self, nsSet: list[BaseNamespace]) -> None:
        self.nsSet = nsSet


    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__.__name__, self.nsSet)


    def __eq__(self, other: Any) -> bool:
        return type(other) == MultinameL and self.nsSet == other.nsSet


    def __hash__(self) -> int:
        return hash((self.kind, *self.nsSet))