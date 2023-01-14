from __future__ import annotations
class UndefinedType(object):
    kind = 0x00

    def __repr__(self) -> str:
        return "Undefined"

Undefined = UndefinedType()