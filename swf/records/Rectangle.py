from __future__ import annotations
from typing import Any


class Rectangle:
    xMin: int
    xMax: int
    yMin: int
    yMax: int

    def __init__(self, xMin: int, xMax: int, yMin: int, yMax: int) -> None:
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax


    def __eq__(self, other: Any) -> bool:
        return type(other) == Rectangle and other.xMin == self.xMin and other.xMax == self.xMax and other.yMin == self.yMin and other.yMax == self.yMax


    def __hash__(self) -> int:
        return hash((self.xMin, self.xMax, self.yMin, self.yMax))