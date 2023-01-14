from __future__ import annotations
from typing import Any


class RGB:
    red: int
    green: int
    blue: int
    
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue


    def __eq__(self, other: Any) -> bool:
        return type(other) == RGB and self.red == other.red and self.green == other.green and self.blue == other.blue
        

    def __hash__(self) -> int:
        return (self.red << 16) + (self.green << 8) + (self.blue)