from __future__ import annotations
from typing import Any
from swf.abc.multinames.BaseMultiname import BaseMultiname
from swf.abc.namespaces.BaseNamespace import BaseNamespace


class QName(BaseMultiname):
    kind = 0x07

    ns: BaseNamespace | None
    name: str | None

    def __init__(self, ns: BaseNamespace | None, name: str | None) -> None:
        self.ns = ns
        self.name = name


    def __repr__(self) -> str:
        return "%s(%r, %r)" % (self.__class__.__name__, self.ns, self.name)


    def __eq__(self, other: Any) -> bool:
        return type(other) == QName and self.name == other.name and self.ns == other.ns


    def __hash__(self) -> int:
        return hash((self.kind, self.ns, self.name))