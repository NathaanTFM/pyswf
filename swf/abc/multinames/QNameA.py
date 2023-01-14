from __future__ import annotations
from typing import Any
from swf.abc.multinames.QName import QName


class QNameA(QName):
    kind = 0x0D
    
    def __eq__(self, other: Any) -> bool:
        return type(other) == QNameA and self.name == other.name and self.ns == other.ns