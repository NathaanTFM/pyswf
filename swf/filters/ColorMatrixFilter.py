from __future__ import annotations
from swf.filters.Filter import Filter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class ColorMatrixFilter(Filter):
    id = 6

    matrix: list[float]

    def __init__(self, matrix: list[float]):
        if len(matrix) != 20:
            raise Exception("bad matrix")

        self.matrix = matrix


    @staticmethod
    def read(stream: SWFInputStream) -> Filter:
        matrix = []
        for _ in range(20):
            matrix.append(stream.readFLOAT())

        return ColorMatrixFilter(matrix)


    def write(self, stream: SWFOutputStream) -> None:
        if len(self.matrix) != 20:
            raise Exception("bad matrix")

        for value in self.matrix:
            stream.writeFLOAT(value)