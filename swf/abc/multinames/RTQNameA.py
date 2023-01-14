from __future__ import annotations
from typing import Any
from swf.abc.multinames.RTQName import RTQName


class RTQNameA(RTQName):
    kind = 0x10

    def __eq__(self, other: Any) -> bool:
        return type(other) == RTQNameA and self.name == other.name