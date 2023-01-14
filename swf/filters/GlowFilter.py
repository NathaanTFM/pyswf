from __future__ import annotations
from swf.records.RGBA import RGBA
from swf.filters.Filter import Filter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class GlowFilter(Filter):
    id = 2

    color: RGBA
    blurX: float
    blurY: float
    strength: float
    innerGlow: bool
    knockout: bool
    compositeSource: bool
    passes: int

    def __init__(self, color: RGBA, blurX: float, blurY: float, strength: float, innerGlow: bool, knockout: bool, compositeSource: bool, passes: int) -> None:
        self.color = color
        self.blurX = blurX
        self.blurY = blurY
        self.strength = strength
        self.innerGlow = innerGlow
        self.knockout = knockout
        self.compositeSource = compositeSource
        self.passes = passes


    @staticmethod
    def read(stream: SWFInputStream) -> Filter:
        color = stream.readRGBA()
        blurX = stream.readFIXED()
        blurY = stream.readFIXED()
        strength = stream.readFIXED8()
        innerGlow = stream.readUB1()
        knockout = stream.readUB1()
        compositeSource = stream.readUB1()
        if not compositeSource:
            raise Exception("composite source is non zero")

        passes = stream.readUB(5)

        return GlowFilter(color, blurX, blurY, strength, innerGlow, knockout, compositeSource, passes)


    def write(self, stream: SWFOutputStream) -> None:
        if not self.compositeSource:
            raise Exception("composite source is not set")

        stream.writeRGBA(self.color)
        stream.writeFIXED(self.blurX)
        stream.writeFIXED(self.blurY)
        stream.writeFIXED8(self.strength)
        stream.writeUB1(self.innerGlow)
        stream.writeUB1(self.knockout)
        stream.writeUB1(self.compositeSource)
        stream.writeUB(5, self.passes)