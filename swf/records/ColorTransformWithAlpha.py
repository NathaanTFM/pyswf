from __future__ import annotations
from typing import Any
from swf.records.ColorTransform import ColorTransform

class ColorTransformWithAlpha(ColorTransform):
    alphaMultTerm: int | None
    alphaAddTerm: int | None

    def __init__(self) -> None:
        super().__init__()
        self.alphaMultTerm = None
        self.alphaAddTerm = None


    def __eq__(self, other: Any) -> bool:
        return (type(other) == ColorTransformWithAlpha
            and other.redMultTerm == self.redMultTerm and other.blueMultTerm == self.blueMultTerm and other.greenMultTerm == self.greenMultTerm
            and other.redAddTerm == self.redAddTerm and other.blueAddTerm == self.blueAddTerm and other.greenMultTerm == self.greenAddTerm
            and other.alphaMultTerm == self.alphaMultTerm and other.alphaAddTerm == self.alphaAddTerm)


    def __hash__(self) -> int:
        return hash((self.redMultTerm, self.blueMultTerm, self.greenMultTerm, self.redAddTerm, self.blueAddTerm, self.greenAddTerm, self.alphaMultTerm, self.alphaAddTerm))