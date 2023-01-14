from __future__ import annotations
from swf.enums.FillStyleType import FillStyleType
from swf.records.RGB import RGB
from swf.records.RGBA import RGBA
from swf.records.Matrix import Matrix
from swf.gradients.Gradient import Gradient
from swf.gradients.FocalGradient import FocalGradient

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class FillStyle:
    type: FillStyleType
    color: RGB | RGBA | None

    gradientMatrix: Matrix | None
    gradient: Gradient | FocalGradient | None

    bitmapId: int | None
    bitmapMatrix: Matrix | None

    def __init__(self, type: FillStyleType, color: RGB | RGBA | None = None, gradientMatrix: Matrix | None = None, gradient: Gradient | FocalGradient | None = None, bitmapId: int | None = None, bitmapMatrix: Matrix | None = None):
        self.type = type
        self.color = color
        self.gradientMatrix = gradientMatrix
        self.gradient = gradient
        self.bitmapId = bitmapId
        self.bitmapMatrix = bitmapMatrix

        if self.type == FillStyleType.SOLID and not self.color:
            raise ValueError("missing color parameter")

        elif self.type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT) and not (self.gradientMatrix and isinstance(self.gradient, Gradient)):
            raise ValueError("missing gradientParameter or bad gradient parameter")

        elif self.type == FillStyleType.FOCAL_GRADIENT and not (self.gradientMatrix and isinstance(self.gradient, FocalGradient)):
            raise ValueError("missing gradientParameter or bad gradient parameter")

        elif self.type in (FillStyleType.REPEATING_BITMAP, FillStyleType.CLIPPED_BITMAP, FillStyleType.NON_SMOOTHED_REPEATING_BITMAP, FillStyleType.NON_SMOOTHED_CLIPPED_BITMAP) and not (self.bitmapId or self.bitmapMatrix):
            raise ValueError("missing bitmapId or bitmapMatrix parameters")


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> FillStyle:
        type = FillStyleType(stream.readUI8())

        color: RGB | RGBA | None = None
        if type == FillStyleType.SOLID:
            if tag >= 3:
                color = stream.readRGBA()
            else:
                color = stream.readRGB()
        
        gradientMatrix = None
        if type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT, FillStyleType.FOCAL_GRADIENT):
            gradientMatrix = stream.readMATRIX()

        gradient: Gradient | FocalGradient | None = None
        if type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT):
            gradient = Gradient.read(stream, tag)

        elif type == FillStyleType.FOCAL_GRADIENT:
            if stream.version < 8:
                raise Exception("bad swf version")

            gradient = FocalGradient.read(stream, tag)

        bitmapId = None
        bitmapMatrix = None
        if type in (FillStyleType.REPEATING_BITMAP, FillStyleType.CLIPPED_BITMAP, FillStyleType.NON_SMOOTHED_REPEATING_BITMAP, FillStyleType.NON_SMOOTHED_CLIPPED_BITMAP):
            bitmapId = stream.readUI16()
            bitmapMatrix = stream.readMATRIX()

        return FillStyle(type, color, gradientMatrix, gradient, bitmapId, bitmapMatrix)


    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUI8(self.type.value)

        if self.type == FillStyleType.SOLID:
            if tag >= 3:
                if type(self.color) != RGBA:
                    raise Exception("expected RGBA color for fill style")

                stream.writeRGBA(self.color)
            else:
                if type(self.color) != RGB:
                    raise Exception("expected RGB color for fill style")

                stream.writeRGB(self.color)

        elif self.type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT, FillStyleType.FOCAL_GRADIENT):
            if type(self.gradientMatrix) != Matrix:
                raise Exception("expected Matrix for fill style")

            stream.writeMATRIX(self.gradientMatrix)
            if self.type in (FillStyleType.LINEAR_GRADIENT, FillStyleType.RADIAL_GRADIENT):
                if type(self.gradient) != Gradient:
                    raise Exception("expected Gradient for fill style")

                self.gradient.write(stream, tag)

            else:
                if type(self.gradient) != FocalGradient:
                    raise Exception("expected Gradient for fill style")

                self.gradient.write(stream, tag)

        
        elif self.type in (FillStyleType.REPEATING_BITMAP, FillStyleType.CLIPPED_BITMAP, FillStyleType.NON_SMOOTHED_REPEATING_BITMAP, FillStyleType.NON_SMOOTHED_CLIPPED_BITMAP):
            if self.bitmapId is None:
                raise Exception("missing bitmapId for fill style")

            if type(self.bitmapMatrix) != Matrix:
                raise Exception("expected Matrix for bitmap fill style")

            stream.writeUI16(self.bitmapId)
            stream.writeMATRIX(self.bitmapMatrix)


    @staticmethod
    def readArray(stream: SWFInputStream, tag: int) -> list[FillStyle]:
        count = stream.readUI8()
        if count == 0xFF and tag >= 2:
            count = stream.readUI16()

        res = []
        for _ in range(count):
            res.append(FillStyle.read(stream, tag))

        return res


    @staticmethod
    def writeArray(stream: SWFOutputStream, array: list[FillStyle], tag: int) -> None:
        if len(array) > 0xFF and tag == 2:
            raise Exception("too long array for swf version")
            
        if len(array) >= 0xFF and tag >= 2:
            stream.writeUI8(0xFF)
            stream.writeUI16(len(array))
        else:
            stream.writeUI8(len(array))

        for elem in array:
            elem.write(stream, tag)