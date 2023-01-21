from __future__ import annotations
from swf.records.RGBA import RGBA
from swf.shapes.LineStyle import LineStyle
from swf.shapes.FillStyle import FillStyle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class LineStyle2(LineStyle):
    startCapStyle: int
    joinStyle: int
    hasFillFlag: bool
    noHScaleFlag: bool
    noVScaleFlag: bool
    pixelHintingFlag: bool
    noClose: bool
    endCapStyle: int
    miterLimitFactor: int | None
    fillType: FillStyle | None

    def __init__(self, width: int, startCapStyle: int, joinStyle: int, hasFillFlag: bool, noHScaleFlag: bool, noVScaleFlag: bool, pixelHintingFlag: bool, noClose: bool, endCapStyle: int, miterLimitFactor: int | None, color: RGBA | None, fillType: FillStyle | None) -> None:
        self.startCapStyle = startCapStyle
        self.joinStyle = joinStyle
        self.hasFillFlag = hasFillFlag
        self.noHScaleFlag = noHScaleFlag
        self.noVScaleFlag = noVScaleFlag
        self.pixelHintingFlag = pixelHintingFlag
        self.noClose = noClose
        self.endCapStyle = endCapStyle
        self.miterLimitFactor = miterLimitFactor
        self.color = color
        self.fillType = fillType

        super().__init__(width, color)


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> LineStyle2:
        width = stream.readUI16()
        startCapStyle = stream.readUB(2)
        joinStyle = stream.readUB(2)
        hasFillFlag = bool(stream.readUB(1))
        noHScaleFlag = bool(stream.readUB(1))
        noVScaleFlag = bool(stream.readUB(1))
        pixelHintingFlag = bool(stream.readUB(1))

        if stream.readUB(5) != 0:
            raise ValueError("reserved is non zero")

        noClose = bool(stream.readUB(1))
        endCapStyle = stream.readUB(2)
        
        miterLimitFactor = None
        if joinStyle == 2:
            miterLimitFactor = stream.readUI16()
        
        color = None
        if hasFillFlag == 0:
            color = stream.readRGBA()
        
        fillType = None
        if hasFillFlag == 1:
            fillType = FillStyle.read(stream, tag)

        return LineStyle2(width, startCapStyle, joinStyle, hasFillFlag, noHScaleFlag, noVScaleFlag, pixelHintingFlag, noClose, endCapStyle, miterLimitFactor, color, fillType)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUI16(self.width)
        stream.writeUB(2, self.startCapStyle)
        stream.writeUB(2, self.joinStyle)
        stream.writeUB(1, self.hasFillFlag)
        stream.writeUB(1, self.noHScaleFlag)
        stream.writeUB(1, self.noVScaleFlag)
        stream.writeUB(1, self.pixelHintingFlag)
        stream.writeUB(5, 0)
        stream.writeUB(1, self.noClose)
        stream.writeUB(2, self.endCapStyle)
        
        if self.joinStyle == 2:
            if self.miterLimitFactor is None:
                raise ValueError("miterLimitFactor is None")

            stream.writeUI16(self.miterLimitFactor)
            
        if self.hasFillFlag == 0:
            if type(self.color) != RGBA:
                raise ValueError("color is not RGBA")

            stream.writeRGBA(self.color)
            
        if self.hasFillFlag == 1:
            if self.fillType is None:
                raise ValueError("fillType is None")

            self.fillType.write(stream, tag)


    @staticmethod
    def readArray(stream: SWFInputStream, tag: int) -> list[LineStyle]: 
        count = stream.readUI8()
        if count == 0xFF:
            count = stream.readUI16()

        res: list[LineStyle] = []
        for _ in range(count):
            res.append(LineStyle2.read(stream, tag))

        return res


    @staticmethod
    def writeArray(stream: SWFOutputStream, array: list[LineStyle], tag: int) -> None:
        if len(array) >= 0xFF:
            stream.writeUI8(0xFF)
            stream.writeUI16(len(array))
        else:
            stream.writeUI8(len(array))

        for elem in array:
            if type(elem) != LineStyle2:
                raise ValueError("expected LineStyle2")

            elem.write(stream, tag)