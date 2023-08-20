from __future__ import annotations
from swf.records.RGBA import RGBA

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class MorphLineStyle:
    startWidth: int
    endWidth: int
    startColor: RGBA
    endColor: RGBA

    def __init__(self, startWidth: int, endWidth: int, startColor: RGBA, endColor: RGBA):
        self.startWidth = startWidth
        self.endWidth = endWidth
        self.startColor = startColor
        self.endColor = endColor


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> MorphLineStyle:
        startWidth = stream.readUI16()
        endWidth = stream.readUI16()

        startColor = stream.readRGBA()
        endColor = stream.readRGBA()

        return MorphLineStyle(startWidth, endWidth, startColor, endColor)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUI16(self.startWidth)
        stream.writeUI16(self.endWidth)
        stream.writeRGBA(self.startColor)
        stream.writeRGBA(self.endColor)


    @staticmethod
    def readArray(stream: SWFInputStream, tag: int) -> list[MorphLineStyle]:
        count = stream.readUI8()
        if count == 0xFF:
            count = stream.readUI16()

        res = []
        for _ in range(count):
            res.append(MorphLineStyle.read(stream, tag))

        return res


    @staticmethod
    def writeArray(stream: SWFOutputStream, array: list[MorphLineStyle], tag: int) -> None:
        if len(array) >= 0xFF:
            stream.writeUI8(0xFF)
            stream.writeUI16(len(array))
        else:
            stream.writeUI8(len(array))

        for elem in array:
            elem.write(stream, tag)