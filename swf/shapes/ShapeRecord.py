from __future__ import annotations
from swf.shapes.FillStyle import FillStyle
from swf.shapes.LineStyle import LineStyle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class ShapeRecord:
    @staticmethod
    def read(stream: SWFInputStream, tag: int, numFillBits: int, numLineBits: int) -> ShapeRecord:
        typeFlag = stream.readUB1()
        if typeFlag:
            straightFlag = stream.readUB1()
            if straightFlag:
                numBits = stream.readUB(4)+2
                generalLineFlag = stream.readUB1()

                deltaX = 0
                deltaY = 0
                if generalLineFlag:
                    deltaX = stream.readSB(numBits)
                    deltaY = stream.readSB(numBits)
                else:
                    vertLineFlag = stream.readUB1()
                    if vertLineFlag:
                        deltaY = stream.readSB(numBits)
                    else:
                        deltaX = stream.readSB(numBits)

                return StraightEdgeRecord(deltaX, deltaY)

            else:
                numBits = stream.readUB(4)+2
                controlDeltaX = stream.readSB(numBits)
                controlDeltaY = stream.readSB(numBits)
                anchorDeltaX = stream.readSB(numBits)
                anchorDeltaY = stream.readSB(numBits)

                return CurvedEdgeRecord(controlDeltaX, controlDeltaY, anchorDeltaX, anchorDeltaY)

        else:
            stateNewStyles = stream.readUB1()
            stateLineStyle = stream.readUB1()
            stateFillStyle1 = stream.readUB1()
            stateFillStyle0 = stream.readUB1()
            stateMoveTo = stream.readUB1()

            if not (stateNewStyles or stateLineStyle or stateFillStyle1 or stateFillStyle0 or stateMoveTo):
                return EndShapeRecord()

            moveDeltaX, moveDeltaY = None, None
            if stateMoveTo:
                moveBits = stream.readUB(5)
                moveDeltaX = stream.readSB(moveBits)
                moveDeltaY = stream.readSB(moveBits)
                
            fillStyle0 = None
            if stateFillStyle0:
                fillStyle0 = stream.readUB(numFillBits)
                
            fillStyle1 = None
            if stateFillStyle1:
                fillStyle1 = stream.readUB(numFillBits)
                
            lineStyle = None
            if stateLineStyle:
                lineStyle = stream.readUB(numLineBits)
                
            fillStyles, lineStyles = None, None
            if stateNewStyles:
                # fillstylearray and linestylearray are aligned,
                # so we must realign before reading
                stream.align()
                
                fillStyles = FillStyle.readArray(stream, tag)
                lineStyles = LineStyle.readArray(stream, tag)

            record = StyleChangeRecord(moveDeltaX, moveDeltaY, fillStyle0, fillStyle1, lineStyle, fillStyles, lineStyles)
            return record


    def write(self, stream: SWFOutputStream, tag: int, numFillBits: int, numLineBits: int) -> None:
        raise NotImplementedError()



class EndShapeRecord(ShapeRecord):
    def write(self, stream: SWFOutputStream, tag: int, numFillBits: int, numLineBits: int) -> None:
        stream.writeUB(6, 0)


class StyleChangeRecord(ShapeRecord):
    moveDeltaX: int | None
    moveDeltaY: int | None
    fillStyle0: int | None
    fillStyle1: int | None
    lineStyle: int | None
    fillStyles: list[FillStyle] | None
    lineStyles: list[LineStyle] | None

    _numFillBits: int
    _numLineBits: int

    def __init__(self, moveDeltaX: int | None = None, moveDeltaY: int | None = None, fillStyle0: int | None = None, fillStyle1: int | None = None, lineStyle: int | None = None, fillStyles: list[FillStyle] | None = None, lineStyles: list[LineStyle] | None = None) -> None:
        self.moveDeltaX = moveDeltaX
        self.moveDeltaY = moveDeltaY
        self.fillStyle0 = fillStyle0
        self.fillStyle1 = fillStyle1
        self.lineStyle = lineStyle
        self.fillStyles = fillStyles
        self.lineStyles = lineStyles


    def write(self, stream: SWFOutputStream, tag: int, numFillBits: int, numLineBits: int) -> None:
        stream.writeUB1(False)
        stream.writeUB1(self.fillStyles is not None and self.lineStyles is not None)
        stream.writeUB1(self.lineStyle is not None)
        stream.writeUB1(self.fillStyle1 is not None)
        stream.writeUB1(self.fillStyle0 is not None)
        stream.writeUB1(self.moveDeltaX is not None and self.moveDeltaY is not None)

        if self.moveDeltaX is not None and self.moveDeltaY is not None:
            moveBits = stream.calcSB(self.moveDeltaX, self.moveDeltaY)
            stream.writeUB(5, moveBits)
            stream.writeSB(moveBits, self.moveDeltaX)
            stream.writeSB(moveBits, self.moveDeltaY)

        if self.fillStyle0 is not None:
            stream.writeUB(numFillBits, self.fillStyle0)

        if self.fillStyle1 is not None:
            stream.writeUB(numFillBits, self.fillStyle1)

        if self.lineStyle is not None:
            stream.writeUB(numLineBits, self.lineStyle)

        if self.fillStyles is not None and self.lineStyles is not None:
            stream.align()

            FillStyle.writeArray(stream, self.fillStyles, tag)
            LineStyle.writeArray(stream, self.lineStyles, tag)


class StraightEdgeRecord(ShapeRecord):
    deltaX: int
    deltaY: int

    def __init__(self, deltaX: int, deltaY: int) -> None:
        self.deltaX = deltaX
        self.deltaY = deltaY


    def write(self, stream: SWFOutputStream, tag: int, numFillBits: int, numLineBits: int) -> None:
        stream.writeUB1(True)
        stream.writeUB1(True)

        numBits = max(2, stream.calcSB(self.deltaX, self.deltaY))
        stream.writeUB(4, numBits-2)

        if self.deltaX == 0:
            stream.writeUB1(False)
            stream.writeUB1(True)
            stream.writeSB(numBits, self.deltaY)

        elif self.deltaY == 0:
            stream.writeUB1(False)
            stream.writeUB1(False)
            stream.writeSB(numBits, self.deltaX)

        else:
            stream.writeUB1(True)
            stream.writeSB(numBits, self.deltaX)
            stream.writeSB(numBits, self.deltaY)



class CurvedEdgeRecord(ShapeRecord):
    controlDeltaX: int
    controlDeltaY: int
    anchorDeltaX: int
    anchorDeltaY: int

    def __init__(self, controlDeltaX: int, controlDeltaY: int, anchorDeltaX: int, anchorDeltaY: int) -> None:
        self.controlDeltaX = controlDeltaX
        self.controlDeltaY = controlDeltaY
        self.anchorDeltaX = anchorDeltaX
        self.anchorDeltaY = anchorDeltaY


    def write(self, stream: SWFOutputStream, tag: int, numFillBits: int, numLineBits: int) -> None:
        stream.writeUB1(True)
        stream.writeUB1(False)

        numBits = max(2, stream.calcSB(self.controlDeltaX, self.controlDeltaY, self.anchorDeltaX, self.anchorDeltaY))
        stream.writeUB(4, numBits-2)

        stream.writeSB(numBits, self.controlDeltaX)
        stream.writeSB(numBits, self.controlDeltaY)
        stream.writeSB(numBits, self.anchorDeltaX)
        stream.writeSB(numBits, self.anchorDeltaY)