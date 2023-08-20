from __future__ import annotations
from swf.records.RGB import RGB
from swf.records.RGBA import RGBA

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFOutputStream import SWFOutputStream
    from swf.stream.SWFInputStream import SWFInputStream
    
class MorphGradientRecord:
    startRatio: int
    startColor: RGBA
    endRatio: int
    endColor: RGBA

    def __init__(self, startRatio: int, startColor: RGBA, endRatio: int, endColor: RGBA):
        self.startRatio = startRatio
        self.startColor = startColor
        self.endRatio = endRatio
        self.endColor = endColor


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> MorphGradientRecord:
        startRatio = stream.readUI8()
        startColor = stream.readRGBA()
        endRatio = stream.readUI8()
        endColor = stream.readRGBA()
        return MorphGradientRecord(startRatio, startColor, endRatio, endColor)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUI8(self.startRatio)
        stream.writeRGBA(self.startColor)
        stream.writeUI8(self.endRatio)
        stream.writeRGBA(self.endColor)
