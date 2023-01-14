from __future__ import annotations
from typing import Any
from swf.abc.multinames.QName import QName
from swf.abc.multinames.BaseMultiname import BaseMultiname


class TypeName(BaseMultiname):
    kind = 0x1D

    qname: QName
    params: list[BaseMultiname]

    def __init__(self, qname: QName, params: list[BaseMultiname]) -> None:
        self.qname = qname
        self.params = params


    def __repr__(self) -> str:
        return "TypeName(%r, %r)" % (self.qname, self.params)


    def __eq__(self, other: Any) -> bool:
        return type(other) == TypeName and self.qname == other.qname and self.params == other.params


    def __hash__(self) -> int:
        return hash((self.kind, self.qname, *self.params))