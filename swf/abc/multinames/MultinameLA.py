from __future__ import annotations
from typing import Any
from swf.abc.multinames.MultinameL import MultinameL


class MultinameLA(MultinameL):
    kind = 0x1C

    def __eq__(self, other: Any) -> bool:
        return type(other) == MultinameLA and self.nsSet == other.nsSet


    def __hash__(self) -> int:
        return hash((self.kind, *self.nsSet))