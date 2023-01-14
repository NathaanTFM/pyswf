from __future__ import annotations
from swf.records.RGBA import RGBA
from swf.filters.Filter import Filter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class BevelFilter(Filter):
    id = 3

    shadowColor: RGBA
    highlightColor: RGBA
    blurX: float
    blurY: float
    angle: float
    distance: float
    strength: float
    innerShadow: bool
    knockout: bool
    compositeSource: bool
    onTop: bool
    passes: int

    def __init__(self, shadowColor: RGBA, highlightColor: RGBA, blurX: float, blurY: float, angle: float, distance: float, strength: float, innerShadow: bool, knockout: bool, compositeSource: bool, onTop: bool, passes: int) -> None:
        self.shadowColor = shadowColor
        self.highlightColor = highlightColor
        self.blurX = blurX
        self.blurY = blurY
        self.angle = angle
        self.distance = distance
        self.strength = strength
        self.innerShadow = innerShadow
        self.knockout = knockout
        self.compositeSource = compositeSource
        self.onTop = onTop
        self.passes = passes


    @staticmethod
    def read(stream: SWFInputStream) -> Filter:
        shadowColor = stream.readRGBA()
        highlightColor = stream.readRGBA()
        blurX = stream.readFIXED()
        blurY = stream.readFIXED()
        angle = stream.readFIXED()
        distance = stream.readFIXED()
        strength = stream.readFIXED8()
        innerShadow = stream.readUB1()
        knockout = stream.readUB1()
        compositeSource = stream.readUB1()
        if not compositeSource:
            raise Exception("composite source is non zero")

        onTop = stream.readUB1()
        passes = stream.readUB(4)

        return BevelFilter(shadowColor, highlightColor, blurX, blurY, angle, distance, strength, innerShadow, knockout, compositeSource, onTop, passes)
        


    def write(self, stream: SWFOutputStream) -> None:
        if not self.compositeSource:
            raise Exception("composite source is not set")

        stream.writeRGBA(self.shadowColor)
        stream.writeRGBA(self.highlightColor)
        stream.writeFIXED(self.blurX)
        stream.writeFIXED(self.blurY)
        stream.writeFIXED(self.angle)
        stream.writeFIXED(self.distance)
        stream.writeFIXED8(self.strength)
        stream.writeUB1(self.innerShadow)
        stream.writeUB1(self.knockout)
        stream.writeUB1(self.compositeSource)
        stream.writeUB1(self.onTop)
        stream.writeUB(4, self.passes)