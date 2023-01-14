from __future__ import annotations
from typing import Any
from swf.abc.multinames.BaseMultiname import BaseMultiname


class RTQNameL(BaseMultiname):
    kind = 0x11

    def __repr__(self) -> str:
        return "%s()" % (self.__class__.__name__)


    def __eq__(self, other: Any) -> bool:
        return type(other) == RTQNameL


    def __hash__(self) -> int:
        return hash((self.kind,))