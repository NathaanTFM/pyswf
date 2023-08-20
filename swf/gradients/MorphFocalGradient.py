from __future__ import annotations
from swf.enums.InterpolationMode import InterpolationMode
from swf.enums.SpreadMode import SpreadMode
from swf.gradients.MorphGradientRecord import MorphGradientRecord

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFOutputStream import SWFOutputStream
    from swf.stream.SWFInputStream import SWFInputStream


class MorphFocalGradient:
    spreadMode: SpreadMode
    interpolationMode: InterpolationMode
    gradientRecords: list[MorphGradientRecord]
    startFocalPoint: float
    endFocalPoint: float

    def __init__(self, spreadMode: SpreadMode, interpolationMode: InterpolationMode, gradientRecords: list[MorphGradientRecord], startFocalPoint: float, endFocalPoint: float):
        self.spreadMode = spreadMode
        self.interpolationMode = interpolationMode
        self.gradientRecords = gradientRecords
        self.startFocalPoint = startFocalPoint
        self.endFocalPoint = endFocalPoint


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> MorphFocalGradient:
        spreadMode = SpreadMode(stream.readUB(2))
        interpolationMode = InterpolationMode(stream.readUB(2))
        numGradients = stream.readUB(4)
        gradientRecords = []
        for _ in range(numGradients):
            gradientRecords.append(MorphGradientRecord.read(stream, tag))

        startFocalPoint = stream.readFIXED8()
        endFocalPoint = stream.readFIXED8()

        return MorphFocalGradient(spreadMode, interpolationMode, gradientRecords, startFocalPoint, endFocalPoint)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUB(2, self.spreadMode.value)
        stream.writeUB(2, self.interpolationMode.value)
        stream.writeUB(4, len(self.gradientRecords))
        for record in self.gradientRecords:
            record.write(stream, tag)

        stream.writeFIXED8(self.startFocalPoint)
        stream.writeFIXED8(self.endFocalPoint)