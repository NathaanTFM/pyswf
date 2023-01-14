from __future__ import annotations
from typing import Any
from swf.abc.multinames.RTQNameL import RTQNameL


class RTQNameLA(RTQNameL):
    kind = 0x12

    def __eq__(self, other: Any) -> bool:
        return type(other) == RTQNameLA