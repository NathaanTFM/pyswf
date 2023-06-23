from __future__ import annotations
from typing import Any
from swf.abc.multinames.BaseMultiname import BaseMultiname
from swf.abc.namespaces.BaseNamespace import BaseNamespace


class Multiname(BaseMultiname):
    kind = 0x09

    name: str | None
    nsSet: tuple[BaseNamespace, ...]

    def __init__(self, name: str | None, nsSet: tuple[BaseNamespace, ...]):
        self.name = name
        self.nsSet = nsSet


    def __repr__(self) -> str:
        return "%s(%r, %r)" % (self.__class__.__name__, self.name, self.nsSet)


    def __eq__(self, other: Any) -> bool:
        return type(other) == Multiname and self.name == other.name and self.nsSet == other.nsSet


    def __hash__(self) -> int:
        return hash((self.kind, self.name, *self.nsSet))