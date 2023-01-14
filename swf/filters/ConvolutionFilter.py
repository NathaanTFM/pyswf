from __future__ import annotations
from swf.records.RGBA import RGBA
from swf.filters.Filter import Filter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class ConvolutionFilter(Filter):
    id = 5

    matrixX: int
    matrixY: int
    divisor: float
    bias: float
    matrix: list[float]
    defaultColor: RGBA
    clamp: bool
    preserveAlpha: bool

    def __init__(self, matrixX: int, matrixY: int, divisor: float, bias: float, matrix: list[float], defaultColor: RGBA, clamp: bool, preserveAlpha: bool):
        if len(matrix) != matrixX * matrixY:
            raise Exception("bad matrix")

        self.matrixX = matrixX
        self.matrixY = matrixY
        self.divisor = divisor
        self.bias = bias
        self.matrix = matrix
        self.defaultColor = defaultColor
        self.clamp = clamp
        self.preserveAlpha = preserveAlpha


    @staticmethod
    def read(stream: SWFInputStream) -> Filter:
        matrixX = stream.readUI8()
        matrixY = stream.readUI8()
        divisor = stream.readFLOAT()
        bias = stream.readFLOAT()
        
        matrix = []
        for _ in range(matrixX * matrixY):
            matrix.append(stream.readFLOAT())

        defaultColor = stream.readRGBA()
        if stream.readUB(6) != 0:
            raise Exception("reserved is non null")

        clamp = stream.readUB1()
        preserveAlpha = stream.readUB1()

        return ConvolutionFilter(matrixX, matrixY, divisor, bias, matrix, defaultColor, clamp, preserveAlpha)


    def write(self, stream: SWFOutputStream) -> None:
        stream.writeUI8(self.matrixX)
        stream.writeUI8(self.matrixY)
        stream.writeFLOAT(self.divisor)
        stream.writeFLOAT(self.bias)

        if len(self.matrix) != self.matrixX * self.matrixY:
            raise Exception("bad length for matrix")

        for elem in self.matrix:
            stream.writeFLOAT(elem)

        stream.writeRGBA(self.defaultColor)
        stream.writeUB(6, 0)
        stream.writeUB1(self.clamp)
        stream.writeUB1(self.preserveAlpha)