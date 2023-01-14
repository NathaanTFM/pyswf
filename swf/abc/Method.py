from __future__ import annotations
import enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.abc.MethodBody import MethodBody
    from swf.abc.ValueType import ValueType
    from swf.abc.multinames.QName import QName
    from swf.abc.multinames.TypeName import TypeName

class MethodFlags(enum.Flag):
    NEED_ARGUMENTS = 0x01
    NEED_ACTIVATION = 0x02
    NEED_REST = 0x04
    HAS_OPTIONAL = 0x08
    SET_DXNS = 0x40
    HAS_PARAM_NAMES = 0x80

    # undocumented, but in avmplus
    NATIVE = 0x20
    IGNORE_REST = 0x10


class Param:
    type: QName | TypeName | None
    default: ValueType | None
    name: str | None

    def __init__(self, type: QName | TypeName | None = None, default: ValueType | None = None, name: str | None = None) -> None:
        self.type = type
        self.default = default
        self.name = name


class Method:
    params: list[Param]
    returnType: QName | TypeName | None
    name: str | None
    flags: MethodFlags

    body: MethodBody | None

    def __init__(self, params: list[Param] | None = None, returnType: QName | TypeName | None = None, name: str | None = None, flags: MethodFlags | None = None, body: MethodBody | None = None) -> None:
        self.params = params if params is not None else []
        self.returnType = returnType
        self.name = name
        self.flags = MethodFlags(0) if flags is None else flags
        self.body = body