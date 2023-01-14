from __future__ import annotations
from swf.shapes.FillStyle import FillStyle
from swf.shapes.LineStyle import LineStyle
from swf.shapes.ShapeRecord import EndShapeRecord, ShapeRecord, StyleChangeRecord

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class ShapeWithStyle:
    fillStyles: list[FillStyle]
    lineStyles: list[LineStyle]
    shapeRecords: list[ShapeRecord]

    def __init__(self, fillStyles: list[FillStyle], lineStyles: list[LineStyle], shapeRecords: list[ShapeRecord]):
        self.fillStyles = fillStyles
        self.lineStyles = lineStyles
        self.shapeRecords = shapeRecords
        

    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> ShapeWithStyle:
        fillStyles = FillStyle.readArray(stream, tag)
        lineStyles = LineStyle.readArray(stream, tag)
        
        numFillBits = stream.readUB(4)
        numLineBits = stream.readUB(4)

        shapeRecords: list[ShapeRecord] = []
        while True:
            shapeRecord = ShapeRecord.read(stream, tag, numFillBits, numLineBits)
            shapeRecords.append(shapeRecord)

            if isinstance(shapeRecord, StyleChangeRecord):
                if shapeRecord.fillStyles is not None and shapeRecord.lineStyles is not None: # stateNewStyles
                    numFillBits = stream.readUB(4)
                    numLineBits = stream.readUB(4)

            elif isinstance(shapeRecord, EndShapeRecord):
                break

        stream.align()
        return ShapeWithStyle(fillStyles, lineStyles, shapeRecords)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        FillStyle.writeArray(stream, self.fillStyles, tag)
        LineStyle.writeArray(stream, self.lineStyles, tag)

        numFillBits = stream.calcUB(len(self.fillStyles))
        numLineBits = stream.calcUB(len(self.lineStyles))

        stream.writeUB(4, numFillBits)
        stream.writeUB(4, numLineBits)

        for shapeRecord in self.shapeRecords:
            shapeRecord.write(stream, tag, numFillBits, numLineBits)

            if isinstance(shapeRecord, StyleChangeRecord):
                if shapeRecord.fillStyles is not None and shapeRecord.lineStyles is not None: # stateNewStyles
                    numFillBits = stream.calcUB(len(shapeRecord.fillStyles))
                    numLineBits = stream.calcUB(len(shapeRecord.lineStyles))

                    stream.writeUB(4, numFillBits)
                    stream.writeUB(4, numLineBits)

            elif isinstance(shapeRecord, EndShapeRecord):
                break
            
        stream.align()