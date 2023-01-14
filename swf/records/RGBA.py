from __future__ import annotations
from typing import Any
from swf.records.RGB import RGB

class RGBA(RGB):
    alpha: int

    def __init__(self, red: int, green: int, blue: int, alpha: int) -> None:
        super().__init__(red, green, blue)
        self.alpha = alpha


    def __eq__(self, other: Any) -> bool:
        return type(other) == RGBA and self.red == other.red and self.green == other.green and self.blue == other.blue and self.alpha == other.alpha
        

    def __hash__(self) -> int:
        return (self.red << 24) + (self.green << 16) + (self.blue << 8) + (self.alpha)