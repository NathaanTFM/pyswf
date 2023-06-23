from __future__ import annotations
from typing import Any
from swf.abc.multinames.Multiname import Multiname


class MultinameA(Multiname):
    kind = 0x0E

    def __eq__(self, other: Any) -> bool:
        return type(other) == MultinameA and self.name == other.name and self.nsSet == other.nsSet


    def __hash__(self) -> int:
        return hash((self.kind, self.name, *self.nsSet))