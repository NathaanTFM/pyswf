from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from swf.abc.Class import Class

from swf.abc.traits.Trait import Trait
from swf.abc.multinames.QName import QName

class TraitClass(Trait):
    kind = 0x04

    slotId: int
    classi: Class

    def __init__(self, name: QName, slotId: int, classi: Class) -> None:
        super().__init__(name)
        self.slotId = slotId
        self.classi = classi