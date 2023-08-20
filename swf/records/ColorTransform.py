from __future__ import annotations
from typing import Any


class ColorTransform:
    redMultTerm: int
    greenMultTerm: int
    blueMultTerm: int

    redAddTerm: int
    greenAddTerm: int
    blueAddTerm: int

    def __init__(self, *, redMultTerm: int = 256, greenMultTerm: int = 256, blueMultTerm: int = 256, redAddTerm: int = 0, greenAddTerm: int = 0, blueAddTerm: int = 0) -> None:
        self.redMultTerm = redMultTerm
        self.greenMultTerm = greenMultTerm
        self.blueMultTerm = blueMultTerm

        self.redAddTerm = redAddTerm
        self.greenAddTerm = greenAddTerm
        self.blueAddTerm = blueAddTerm


    def __eq__(self, other: Any) -> bool:
        return (type(other) == ColorTransform
            and other.redMultTerm == self.redMultTerm and other.blueMultTerm == self.blueMultTerm and other.greenMultTerm == self.greenMultTerm
            and other.redAddTerm == self.redAddTerm and other.blueAddTerm == self.blueAddTerm and other.greenMultTerm == self.greenAddTerm)


    def __hash__(self) -> int:
        return hash((self.redMultTerm, self.blueMultTerm, self.greenMultTerm, self.redAddTerm, self.blueAddTerm, self.greenAddTerm))
    

    def __repr__(self) -> str:
        return "ColorTransform(redMultTerm=%r, greenMultTerm=%r, blueMultTerm=%r, redAddTerm=%r, blueAddTerm=%r, greenAddTerm=%r)" % (self.redMultTerm, self.greenMultTerm, self.blueMultTerm, self.redAddTerm, self.greenAddTerm, self.blueAddTerm)
    