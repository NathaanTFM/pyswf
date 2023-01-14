from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from swf.abc.Method import Method

from swf.abc.traits.Trait import Trait
from swf.abc.multinames.QName import QName

class TraitFunction(Trait):
    kind = 0x05

    slotId: int
    function: Method

    def __init__(self, name: QName, slotId: int, function: Method) -> None:
        super().__init__(name)
        self.slotId = slotId
        self.function = function