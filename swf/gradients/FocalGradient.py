from __future__ import annotations
from swf.enums.InterpolationMode import InterpolationMode
from swf.enums.SpreadMode import SpreadMode
from swf.gradients.GradientRecord import GradientRecord

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFOutputStream import SWFOutputStream
    from swf.stream.SWFInputStream import SWFInputStream


class FocalGradient:
    spreadMode: SpreadMode
    interpolationMode: InterpolationMode
    gradientRecords: list[GradientRecord]
    focalPoint: float

    def __init__(self, spreadMode: SpreadMode, interpolationMode: InterpolationMode, gradientRecords: list[GradientRecord], focalPoint: float):
        self.spreadMode = spreadMode
        self.interpolationMode = interpolationMode
        self.gradientRecords = gradientRecords
        self.focalPoint = focalPoint


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> FocalGradient:
        if tag < 4:
            raise Exception("bad tag")

        spreadMode = SpreadMode(stream.readUB(2))
        interpolationMode = InterpolationMode(stream.readUB(2))
        numGradients = stream.readUB(4)
        gradientRecords = []
        for _ in range(numGradients):
            gradientRecords.append(GradientRecord.read(stream, tag))

        focalPoint = stream.readFIXED8()
        return FocalGradient(spreadMode, interpolationMode, gradientRecords, focalPoint)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUB(2, self.spreadMode.value)
        stream.writeUB(2, self.interpolationMode.value)
        stream.writeUB(4, len(self.gradientRecords))
        for record in self.gradientRecords:
            record.write(stream, tag)

        stream.writeFIXED8(self.focalPoint)