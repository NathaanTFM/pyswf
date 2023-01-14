from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from swf.abc.Method import Method

from swf.abc.traits.Trait import Trait
from swf.abc.multinames.QName import QName

class TraitMethod(Trait):
    kind = 0x01

    dispId: int
    method: Method
    final: bool
    override: bool

    def __init__(self, name: QName, dispId: int, method: Method, final: bool, override: bool) -> None:
        super().__init__(name)
        self.dispId = dispId
        self.method = method
        self.final = final
        self.override = override