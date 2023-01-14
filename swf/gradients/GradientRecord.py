from __future__ import annotations
from swf.records.RGB import RGB
from swf.records.RGBA import RGBA

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFOutputStream import SWFOutputStream
    from swf.stream.SWFInputStream import SWFInputStream
    
class GradientRecord:
    ratio: int
    color: RGB | RGBA

    def __init__(self, ratio: int, color: RGB | RGBA):
        self.ratio = ratio
        self.color = color

    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> GradientRecord:
        ratio = stream.readUI8()
        color: RGB | RGBA
        if tag >= 3:
            color = stream.readRGBA()
        else:
            color = stream.readRGB()

        return GradientRecord(ratio, color)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUI8(self.ratio)
        if tag >= 3:
            if type(self.color) != RGBA:
                raise Exception("expected RGBA")

            stream.writeRGBA(self.color)

        else:
            if type(self.color) != RGB:
                raise Exception("expected RGB")

            stream.writeRGB(self.color)