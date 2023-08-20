from __future__ import annotations
from swf.records.RGBA import RGBA
from swf.shapes.MorphFillStyle import MorphFillStyle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class MorphLineStyle2:
    startWidth: int
    endWidth: int
    startCapStyle: int
    joinStyle: int
    hasFillFlag: bool
    noHScaleFlag: bool
    noVScaleFlag: bool
    pixelHintingFlag: bool
    noClose: bool
    endCapStyle: int
    miterLimitFactor: int | None
    startColor: RGBA | None
    endColor: RGBA | None
    fillType: MorphFillStyle | None

    def __init__(self, startWidth: int, endWidth: int, startCapStyle: int, joinStyle: int, hasFillFlag: bool, noHScaleFlag: bool, noVScaleFlag: bool, pixelHintingFlag: bool, noClose: bool, endCapStyle: int, miterLimitFactor: int | None, startColor: RGBA | None, endColor: RGBA | None, fillType: MorphFillStyle | None) -> None:
        self.startWidth = startWidth
        self.endWidth = endWidth
        self.startCapStyle = startCapStyle
        self.joinStyle = joinStyle
        self.hasFillFlag = hasFillFlag
        self.noHScaleFlag = noHScaleFlag
        self.noVScaleFlag = noVScaleFlag
        self.pixelHintingFlag = pixelHintingFlag
        self.noClose = noClose
        self.endCapStyle = endCapStyle
        self.miterLimitFactor = miterLimitFactor
        self.startColor = startColor
        self.endColor = endColor
        self.fillType = fillType


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> MorphLineStyle2:
        startWidth = stream.readUI16()
        endWidth = stream.readUI16()
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
        
        startColor = endColor = None
        if hasFillFlag == 0:
            startColor = stream.readRGBA()
            endColor = stream.readRGBA()
        
        fillType = None
        if hasFillFlag == 1:
            fillType = MorphFillStyle.read(stream, tag)

        return MorphLineStyle2(startWidth, endWidth, startCapStyle, joinStyle, hasFillFlag, noHScaleFlag, noVScaleFlag, pixelHintingFlag, noClose, endCapStyle, miterLimitFactor, startColor, endColor, fillType)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUI16(self.startWidth)
        stream.writeUI16(self.endWidth)
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
            if type(self.startColor) != RGBA:
                raise ValueError("startColor is not RGBA")
            
            if type(self.endColor) != RGBA:
                raise ValueError("endColor is not RGBA")

            stream.writeRGBA(self.startColor)
            stream.writeRGBA(self.endColor)
            
        if self.hasFillFlag == 1:
            if self.fillType is None:
                raise ValueError("fillType is None")

            self.fillType.write(stream, tag)


    @staticmethod
    def readArray(stream: SWFInputStream, tag: int) -> list[MorphLineStyle2]: 
        count = stream.readUI8()
        if count == 0xFF:
            count = stream.readUI16()

        res: list[MorphLineStyle2] = []
        for _ in range(count):
            res.append(MorphLineStyle2.read(stream, tag))

        return res


    @staticmethod
    def writeArray(stream: SWFOutputStream, array: list[MorphLineStyle2], tag: int) -> None:
        if len(array) >= 0xFF:
            stream.writeUI8(0xFF)
            stream.writeUI16(len(array))
        else:
            stream.writeUI8(len(array))

        for elem in array:
            elem.write(stream, tag)