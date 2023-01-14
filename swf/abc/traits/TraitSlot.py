from __future__ import annotations
from swf.abc.constants.Undefined import Undefined
from swf.abc.traits.Trait import Trait

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.abc.ValueType import ValueType
    from swf.abc.multinames.QName import QName
    from swf.abc.multinames.TypeName import TypeName

class TraitSlot(Trait):
    kind = 0x00

    slotId: int
    type: QName | TypeName | None
    value: ValueType

    def __init__(self, name: QName, slotId: int, type: QName | TypeName | None = None, value: ValueType = Undefined):
        super().__init__(name)
        self.slotId = slotId
        self.type = type
        self.value = value