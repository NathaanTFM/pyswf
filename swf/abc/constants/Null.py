from __future__ import annotations
class NullType(object):
    kind = 0x0C

    def __repr__(self) -> str:
        return "Null"

Null = NullType()