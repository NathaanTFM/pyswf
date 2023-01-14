from __future__ import annotations
from swf.filters.Filter import Filter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class BlurFilter(Filter):
    id = 1

    blurX: float
    blurY: float
    passes: int

    def __init__(self, blurX: float, blurY: float, passes: int) -> None:
        self.blurX = blurX
        self.blurY = blurY
        self.passes = passes


    @staticmethod
    def read(stream: SWFInputStream) -> Filter:
        blurX = stream.readFIXED()
        blurY = stream.readFIXED()
        passes = stream.readUB(5)
        if stream.readUB(3) != 0:
            raise Exception("reserved is non zero")

        return BlurFilter(blurX, blurY, passes)


    def write(self, stream: SWFOutputStream) -> None:
        stream.writeFIXED(self.blurX)
        stream.writeFIXED(self.blurY)
        stream.writeUB(5, self.passes)
        stream.writeUB(3, 0)