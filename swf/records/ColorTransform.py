from __future__ import annotations
from typing import Any


class ColorTransform:
    redMultTerm: int | None
    greenMultTerm: int | None
    blueMultTerm: int | None

    redAddTerm: int | None
    greenAddTerm: int | None
    blueAddTerm: int | None

    def __init__(self) -> None:
        self.redMultTerm = None
        self.greenMultTerm = None
        self.blueMultTerm = None

        self.redAddTerm = None
        self.greenAddTerm = None
        self.blueAddTerm = None


    def __eq__(self, other: Any) -> bool:
        return (type(other) == ColorTransform
            and other.redMultTerm == self.redMultTerm and other.blueMultTerm == self.blueMultTerm and other.greenMultTerm == self.greenMultTerm
            and other.redAddTerm == self.redAddTerm and other.blueAddTerm == self.blueAddTerm and other.greenMultTerm == self.greenAddTerm)


    def __hash__(self) -> int:
        return hash((self.redMultTerm, self.blueMultTerm, self.greenMultTerm, self.redAddTerm, self.blueAddTerm, self.greenAddTerm))