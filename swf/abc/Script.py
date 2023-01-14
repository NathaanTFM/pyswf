from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.abc.traits.Trait import Trait
    from swf.abc.Method import Method

class Script:
    init: Method
    traits: list[Trait]

    def __init__(self) -> None:
        self.traits = []