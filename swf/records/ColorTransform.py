from __future__ import annotations
from typing import Any


class ColorTransform:
    redMultTerm: int
    greenMultTerm: int
    blueMultTerm: int

    redAddTerm: int
    greenAddTerm: int
    blueAddTerm: int

    def __init__(self) -> None:
        self.redMultTerm = 256
        self.greenMultTerm = 256
        self.blueMultTerm = 256

        self.redAddTerm = 0
        self.greenAddTerm = 0
        self.blueAddTerm = 0


    def __eq__(self, other: Any) -> bool:
        return (type(other) == ColorTransform
            and other.redMultTerm == self.redMultTerm and other.blueMultTerm == self.blueMultTerm and other.greenMultTerm == self.greenMultTerm
            and other.redAddTerm == self.redAddTerm and other.blueAddTerm == self.blueAddTerm and other.greenMultTerm == self.greenAddTerm)


    def __hash__(self) -> int:
        return hash((self.redMultTerm, self.blueMultTerm, self.greenMultTerm, self.redAddTerm, self.blueAddTerm, self.greenAddTerm))