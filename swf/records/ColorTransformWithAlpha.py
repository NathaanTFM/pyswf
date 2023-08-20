from __future__ import annotations
from typing import Any
from swf.records.ColorTransform import ColorTransform

class ColorTransformWithAlpha(ColorTransform):
    alphaMultTerm: int
    alphaAddTerm: int

    def __init__(self, redMultTerm: int = 256, greenMultTerm: int = 256, blueMultTerm: int = 256, alphaMultTerm: int = 256, redAddTerm: int = 0, greenAddTerm: int = 0, blueAddTerm: int = 0, alphaAddTerm: int = 0) -> None:
        super().__init__(redMultTerm=redMultTerm, greenMultTerm=greenMultTerm, blueMultTerm=blueMultTerm, redAddTerm=redAddTerm, greenAddTerm=greenAddTerm, blueAddTerm=blueAddTerm)
        self.alphaMultTerm = alphaMultTerm
        self.alphaAddTerm = alphaAddTerm


    def __eq__(self, other: Any) -> bool:
        return (type(other) == ColorTransformWithAlpha
            and other.redMultTerm == self.redMultTerm and other.blueMultTerm == self.blueMultTerm and other.greenMultTerm == self.greenMultTerm
            and other.redAddTerm == self.redAddTerm and other.blueAddTerm == self.blueAddTerm and other.greenMultTerm == self.greenAddTerm
            and other.alphaMultTerm == self.alphaMultTerm and other.alphaAddTerm == self.alphaAddTerm)


    def __hash__(self) -> int:
        return hash((self.redMultTerm, self.blueMultTerm, self.greenMultTerm, self.redAddTerm, self.blueAddTerm, self.greenAddTerm, self.alphaMultTerm, self.alphaAddTerm))


    def __repr__(self) -> str:
        return "ColorTransformWithAlpha(redMultTerm=%r, greenMultTerm=%r, blueMultTerm=%r, alphaMultTerm=%r, redAddTerm=%r, blueAddTerm=%r, greenAddTerm=%r, alphaAddTerm=%r)" % (self.redMultTerm, self.greenMultTerm, self.blueMultTerm, self.alphaMultTerm, self.redAddTerm, self.greenAddTerm, self.blueAddTerm, self.alphaAddTerm)
    