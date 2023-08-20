from __future__ import annotations
from swf.enums.FillStyleType import FillStyleType
from swf.records.RGB import RGB
from swf.records.RGBA import RGBA
from swf.records.Matrix import Matrix
from swf.gradients.MorphGradient import MorphGradient
from swf.gradients.MorphFocalGradient import MorphFocalGradient

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class MorphFillStyle:
    type: FillStyleType
    startColor: RGBA | None
    endColor: RGBA | None

    startGradientMatrix: Matrix | None
    endGradientMatrix: Matrix | None
    gradient: MorphGradient | MorphFocalGradient | None

    bitmapId: int | None
    startBitmapMatrix: Matrix | None
    endBitmapMatrix: Matrix | None

    def __init__(self, type: FillStyleType, startColor: RGBA | None = None, endColor: RGBA | None = None, startGradientMatrix: Matrix | None = None, endGradientMatrix: Matrix | None = None, gradient: MorphGradient | MorphFocalGradient | None = None, bitmapId: int | None = None, startBitmapMatrix: Matrix | None = None, endBitmapMatrix: Matrix | None = None):
        self.type = type
        self.startColor = startColor
        self.endColor = endColor
        self.startGradientMatrix = startGradientMatrix
        self.endGradientMatrix = endGradientMatrix
        self.gradient = gradient
        self.bitmapId = bitmapId
        self.startBitmapMatrix = startBitmapMatrix
        self.endBitmapMatrix = endBitmapMatrix

        if self.type == FillStyleType.SOLID and not (self.startColor and self.endColor):
            raise ValueError("missing color parameter")

        elif self.type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT) and not (self.startGradientMatrix and self.endGradientMatrix and isinstance(self.gradient, MorphGradient)):
            raise ValueError("missing gradientParameter or bad gradient parameter")

        elif self.type == FillStyleType.FOCAL_GRADIENT and not (self.startGradientMatrix and self.endGradientMatrix and isinstance(self.gradient, MorphFocalGradient)):
            raise ValueError("missing gradientParameter or bad gradient parameter")

        elif self.type in (FillStyleType.REPEATING_BITMAP, FillStyleType.CLIPPED_BITMAP, FillStyleType.NON_SMOOTHED_REPEATING_BITMAP, FillStyleType.NON_SMOOTHED_CLIPPED_BITMAP) and not (self.bitmapId and self.startBitmapMatrix and self.endGradientMatrix):
            raise ValueError("missing bitmapId or bitmapMatrix parameters")


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> MorphFillStyle:
        type = FillStyleType(stream.readUI8())

        startColor: RGBA | None = None
        endColor: RGBA | None = None
        if type == FillStyleType.SOLID:
            startColor = stream.readRGBA()
            endColor = stream.readRGBA()
        
        startGradientMatrix = None
        endGradientMatrix = None
        if type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT, FillStyleType.FOCAL_GRADIENT):
            startGradientMatrix = stream.readMATRIX()
            endGradientMatrix = stream.readMATRIX()

        gradient: MorphGradient | MorphFocalGradient | None = None
        if type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT):
            gradient = MorphGradient.read(stream, tag)

        elif type == FillStyleType.FOCAL_GRADIENT:
            if stream.version < 8:
                raise Exception("bad swf version")

            gradient = MorphFocalGradient.read(stream, tag)

        bitmapId = None
        startBitmapMatrix = None
        endBitmapMatrix = None
        if type in (FillStyleType.REPEATING_BITMAP, FillStyleType.CLIPPED_BITMAP, FillStyleType.NON_SMOOTHED_REPEATING_BITMAP, FillStyleType.NON_SMOOTHED_CLIPPED_BITMAP):
            bitmapId = stream.readUI16()
            startBitmapMatrix = stream.readMATRIX()
            endBitmapMatrix = stream.readMATRIX()

        return MorphFillStyle(type, startColor, endColor, startGradientMatrix, endGradientMatrix, gradient, bitmapId, startBitmapMatrix, endBitmapMatrix)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUI8(self.type.value)

        if self.type == FillStyleType.SOLID:
            if type(self.startColor) != RGBA:
                raise Exception("expected RGBA color for fill style")
            
            if type(self.endColor) != RGBA:
                raise Exception("expected RGBA color for fill style")

            stream.writeRGBA(self.startColor)
            stream.writeRGBA(self.endColor)

        elif self.type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT, FillStyleType.FOCAL_GRADIENT):
            if type(self.startGradientMatrix) != Matrix:
                raise Exception("expected Matrix for fill style")
            
            if type(self.endGradientMatrix) != Matrix:
                raise Exception("expected Matrix for fill style")

            stream.writeMATRIX(self.startGradientMatrix)
            stream.writeMATRIX(self.endGradientMatrix)

            if self.type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT):
                if type(self.gradient) != MorphGradient:
                    raise Exception("expected Gradient for fill style")

                self.gradient.write(stream, tag)

            else:
                if type(self.gradient) != MorphFocalGradient:
                    raise Exception("expected Gradient for fill style")

                self.gradient.write(stream, tag)

        
        elif self.type in (FillStyleType.REPEATING_BITMAP, FillStyleType.CLIPPED_BITMAP, FillStyleType.NON_SMOOTHED_REPEATING_BITMAP, FillStyleType.NON_SMOOTHED_CLIPPED_BITMAP):
            if self.bitmapId is None:
                raise Exception("missing bitmapId for fill style")

            if type(self.startBitmapMatrix) != Matrix:
                raise Exception("expected Matrix for bitmap fill style")

            if type(self.endBitmapMatrix) != Matrix:
                raise Exception("expected Matrix for bitmap fill style")

            stream.writeUI16(self.bitmapId)
            stream.writeMATRIX(self.startBitmapMatrix)
            stream.writeMATRIX(self.endBitmapMatrix)


    @staticmethod
    def readArray(stream: SWFInputStream, tag: int) -> list[MorphFillStyle]:
        count = stream.readUI8()
        if count == 0xFF:
            count = stream.readUI16()

        res = []
        for _ in range(count):
            res.append(MorphFillStyle.read(stream, tag))

        return res


    @staticmethod
    def writeArray(stream: SWFOutputStream, array: list[MorphFillStyle], tag: int) -> None:
        if len(array) >= 0xFF:
            stream.writeUI8(0xFF)
            stream.writeUI16(len(array))
        else:
            stream.writeUI8(len(array))

        for elem in array:
            elem.write(stream, tag)