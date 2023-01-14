from __future__ import annotations
from typing import Any


class Matrix:
    scaleX: float | None
    scaleY: float | None

    rotateSkew0: float | None
    rotateSkew1: float | None

    translateX: int
    translateY: int
    
    def __init__(self, translateX: int, translateY: int):
        self.scaleX = None
        self.scaleY = None
        self.rotateSkew0 = None
        self.rotateSkew1 = None
        self.translateX = translateX
        self.translateY = translateY


    def __eq__(self, other: Any) -> bool:
        return (type(other) == Matrix
            and other.scaleX == self.scaleX and other.scaleY == self.scaleY
            and other.rotateSkew0 == self.rotateSkew0 and other.rotateSkew1 == self.rotateSkew1
            and other.translateX == self.translateX and other.translateY == self.translateY)


    def __hash__(self) -> int:
        return hash((self.scaleX, self.scaleY, self.rotateSkew0, self.rotateSkew1, self.translateX, self.translateY))