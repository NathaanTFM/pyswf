from __future__ import annotations
from swf.records.RGB import RGB
from swf.records.RGBA import RGBA

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class LineStyle:
    width: int
    color: RGB | RGBA

    def __init__(self, width: int, color: RGB | RGBA):
        self.width = width
        self.color = color


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> LineStyle:
        width = stream.readUI16()

        color: RGB | RGBA
        if tag >= 3:
            color = stream.readRGBA()
        else:
            color = stream.readRGB()

        return LineStyle(width, color)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUI16(self.width)
        if tag >= 3:
            if type(self.color) != RGBA:
                raise Exception("expected RGBA")

            stream.writeRGBA(self.color)

        else:
            if type(self.color) != RGB:
                raise Exception("expected RGB")

            stream.writeRGB(self.color)


    @staticmethod
    def readArray(stream: SWFInputStream, tag: int) -> list[LineStyle]:
        count = stream.readUI8()
        if count == 0xFF:
            count = stream.readUI16()

        res = []
        for _ in range(count):
            res.append(LineStyle.read(stream, tag))

        return res


    @staticmethod
    def writeArray(stream: SWFOutputStream, array: list[LineStyle], tag: int) -> None:
        if len(array) >= 0xFF:
            stream.writeUI8(0xFF)
            stream.writeUI16(len(array))
        else:
            stream.writeUI8(len(array))

        for elem in array:
            elem.write(stream, tag)