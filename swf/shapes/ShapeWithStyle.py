from __future__ import annotations
from swf.shapes.MorphFillStyle import MorphFillStyle
from swf.shapes.MorphLineStyle import MorphLineStyle
from swf.shapes.MorphLineStyle2 import MorphLineStyle2
from swf.shapes.FillStyle import FillStyle
from swf.shapes.LineStyle import LineStyle
from swf.shapes.LineStyle2 import LineStyle2
from swf.shapes.ShapeRecord import EndShapeRecord, ShapeRecord, StyleChangeRecord

from typing import TYPE_CHECKING, TypeVar, Generic, Type
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

F = TypeVar("F", FillStyle, MorphFillStyle)
L = TypeVar("L", LineStyle, LineStyle2, MorphLineStyle, MorphLineStyle2)

class ShapeWithStyle(Generic[F, L]):
    fillStyles: list[F]
    lineStyles: list[L]
    shapeRecords: list[ShapeRecord[F, L]]

    def __init__(self, fillStyles: list[F], lineStyles: list[L], shapeRecords: list[ShapeRecord[F, L]]):
        self.fillStyles = fillStyles
        self.lineStyles = lineStyles
        self.shapeRecords = shapeRecords
        

    @staticmethod
    def read(stream: SWFInputStream, tag: int, fillStyleType: Type[F], lineStyleType: Type[L]) -> ShapeWithStyle[F, L]:
        fillStyles: list[F] = fillStyleType.readArray(stream, tag)
        lineStyles: list[L] = lineStyleType.readArray(stream, tag)
        
        numFillBits = stream.readUB(4)
        numLineBits = stream.readUB(4)

        shapeRecords: list[ShapeRecord[F, L]] = []
        while True:
            shapeRecord = ShapeRecord.read(stream, tag, numFillBits, numLineBits, fillStyleType, lineStyleType)
            shapeRecords.append(shapeRecord)

            if isinstance(shapeRecord, StyleChangeRecord):
                if shapeRecord.fillStyles is not None and shapeRecord.lineStyles is not None: # stateNewStyles
                    numFillBits = stream.readUB(4)
                    numLineBits = stream.readUB(4)

            elif isinstance(shapeRecord, EndShapeRecord):
                break

        stream.align()
        return ShapeWithStyle(fillStyles, lineStyles, shapeRecords)


    def write(self, stream: SWFOutputStream, tag: int, fillStyleType: Type[F], lineStyleType: Type[L]) -> None:
        fillStyleType.writeArray(stream, self.fillStyles, tag)
        lineStyleType.writeArray(stream, self.lineStyles, tag)

        numFillBits = stream.calcUB(len(self.fillStyles))
        numLineBits = stream.calcUB(len(self.lineStyles))

        stream.writeUB(4, numFillBits)
        stream.writeUB(4, numLineBits)

        for shapeRecord in self.shapeRecords:
            shapeRecord.write(stream, tag, numFillBits, numLineBits, fillStyleType, lineStyleType)

            if isinstance(shapeRecord, StyleChangeRecord):
                if shapeRecord.fillStyles is not None and shapeRecord.lineStyles is not None: # stateNewStyles
                    numFillBits = stream.calcUB(len(shapeRecord.fillStyles))
                    numLineBits = stream.calcUB(len(shapeRecord.lineStyles))

                    stream.writeUB(4, numFillBits)
                    stream.writeUB(4, numLineBits)

            elif isinstance(shapeRecord, EndShapeRecord):
                break
            
        stream.align()