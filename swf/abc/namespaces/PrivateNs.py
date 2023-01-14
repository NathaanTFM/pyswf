from __future__ import annotations
from typing import Any
from swf.abc.namespaces.BaseNamespace import BaseNamespace

class PrivateNs(BaseNamespace):
    kind = 0x05

    def __eq__(self, other: Any) -> bool:
        return self is other


    def __hash__(self) -> int:
        return id(self)