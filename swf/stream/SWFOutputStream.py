from __future__ import annotations
import math

import struct
from swf.enums.LanguageCode import LanguageCode
from swf.records.RGB import RGB
from swf.records.RGBA import RGBA
from swf.records.Rectangle import Rectangle
from swf.records.Matrix import Matrix
from swf.records.ColorTransform import ColorTransform
from swf.records.ColorTransformWithAlpha import ColorTransformWithAlpha


class SWFOutputStream:
    version: int

    def __init__(self, version: int) -> None:
        self.version = version
        self.__data = bytearray()
        self.__bitposition = 0

    
    def getBytes(self) -> bytes:
        return bytes(self.__data)

    
    def getLength(self) -> int:
        return len(self.__data)


    def write(self, data: bytes) -> None:
        """
        Append bytes at the end of the buffer
        """
        assert self.__bitposition == 0
        self.__data.extend(data)


    def writeSI8(self, value: int) -> None:
        self.write(struct.pack("<b", value))


    def writeSI16(self, value: int) -> None:
        self.write(struct.pack("<h", value))


    def writeSI32(self, value: int) -> None:
        self.write(struct.pack("<i", value))


    def writeUI8(self, value: int) -> None:
        self.write(struct.pack("<B", value))


    def writeUI16(self, value: int) -> None:
        self.write(struct.pack("<H", value))


    def writeUI32(self, value: int) -> None:
        self.write(struct.pack("<I", value))


    def writeUI64(self, value: int) -> None:
        self.write(struct.pack("<Q", value))


    def writeFIXED(self, value: float) -> None:
        self.writeUI32(round(value * 65536))


    def writeFIXED8(self, value: float) -> None:
        self.writeUI16(round(value * 256))


    def writeFLOAT16(self, value: float) -> None:
        if value == 0:
            self.writeUI16(0)
            return

        mantissa, exponent = math.frexp(value)
        mantissa = round(((mantissa * 2) - 1) * 0x400)
        exponent = (exponent - 1) + 16
        assert 0 <= exponent <= 31

        self.writeUI16((0x8000 if mantissa < 0 else 0) | (exponent << 10) | abs(mantissa))
        

    def writeFLOAT(self, value: float) -> None:
        self.write(struct.pack("<f", value))
        

    def writeDOUBLE(self, value: float) -> None:
        self.write(struct.pack("<d", value))


    def writeEncodedU32(self, value: int) -> None:
        assert 0 <= value <= 0xFFFFFFFF
        while True:
            byte = value & 0x7F
            value >>= 7

            self.writeUI8(byte | (0x80 if value else 0))
            if not value:
                break


    def writeUB(self, length: int, value: int) -> None:
        assert 0 <= value < (2 ** length)
        while length:
            if not self.__bitposition:
                self.__data.append(0)

            avail = 8 - self.__bitposition
            if length >= avail:
                length -= avail
                self.__data[-1] |= (value >> length) & ((1 << avail) - 1)
                self.__bitposition = 0

            else:
                self.__data[-1] |= (value & ((1 << length) - 1)) << (avail - length)
                self.__bitposition += length
                break


    def writeSB(self, length: int, value: int) -> None:
        assert -(2 ** (length-1)) <= value < (2 ** (length-1))
        if value < 0:
            value += (1 << length)
        
        self.writeUB(length, value)


    def writeFB(self, length: int, value: float) -> None:
        self.writeSB(length, round(value * 65536))

    
    def writeUB1(self, value: bool) -> None:
        self.writeUB(1, 1 if value else 0)


    def calcUB(self, *values: int) -> int:
        res = 0
        for value in values:
            if value != 0:
                res = max(math.floor(math.log2(value) + 1), res)

        return res


    def calcSB(self, *values: int) -> int:
        res = 0
        for value in values:
            if value < 0:
                res = max(math.ceil(math.log2(-value) + 1), res)
            elif value > 0:
                res = max(math.floor(math.log2(value) + 2), res)

        return res


    def calcFB(self, *values: float) -> int:
        return self.calcSB(*[round(value * 65536) for value in values])


    def align(self) -> None:
        if self.__bitposition:
            self.__bitposition = 0


    def writeString(self, value: str) -> None:
        if "\0" in value:
            raise Exception("cannot have NULL byte")
            
        if self.version >= 6:
            self.write(value.encode("utf8"))
        else:
            self.write(value.encode("ansi"))

        self.writeUI8(0)


    def writeLanguageCode(self, value: LanguageCode) -> None:
        self.writeUI8(value.value)


    def writeRGB(self, value: RGB) -> None:
        self.writeUI8(value.red)
        self.writeUI8(value.green)
        self.writeUI8(value.blue)


    def writeRGBA(self, value: RGBA) -> None:
        self.writeUI8(value.red)
        self.writeUI8(value.green)
        self.writeUI8(value.blue)
        self.writeUI8(value.alpha)


    def writeARGB(self, value: RGBA) -> None:
        self.writeUI8(value.alpha)
        self.writeUI8(value.red)
        self.writeUI8(value.green)
        self.writeUI8(value.blue)


    def writeRECT(self, value: Rectangle) -> None:
        nbits = self.calcSB(value.xMin, value.xMax, value.yMin, value.yMax)
        self.writeUB(5, nbits)
        self.writeSB(nbits, value.xMin)
        self.writeSB(nbits, value.xMax)
        self.writeSB(nbits, value.yMin)
        self.writeSB(nbits, value.yMax)
        self.align()


    def writeMATRIX(self, value: Matrix) -> None:
        if value.scaleX != 1.0 and value.scaleY != 1.0:
            nScaleBits = self.calcFB(value.scaleX, value.scaleY)
            self.writeUB1(True)
            self.writeUB(5, nScaleBits)
            self.writeFB(nScaleBits, value.scaleX)
            self.writeFB(nScaleBits, value.scaleY)

        else:
            self.writeUB1(False)
            
        if value.rotateSkew0 != 0.0 and value.rotateSkew1 != 0.0:
            nRotateBits = self.calcFB(value.rotateSkew0, value.rotateSkew1)
            self.writeUB1(True)
            self.writeUB(5, nRotateBits)
            self.writeFB(nRotateBits, value.rotateSkew0)
            self.writeFB(nRotateBits, value.rotateSkew1)
        else:
            self.writeUB1(False)

        nTranslateBits = self.calcSB(value.translateX, value.translateY)
        self.writeUB(5, nTranslateBits)
        self.writeSB(nTranslateBits, value.translateX)
        self.writeSB(nTranslateBits, value.translateY)
        self.align()


    def writeCXFORM(self, value: ColorTransform) -> None:
        hasMultTerms = value.redMultTerm != 256 and value.greenMultTerm != 256 and value.blueMultTerm != 256
        hasAddTerms = value.redAddTerm != 0 and value.greenAddTerm != 0 and value.blueAddTerm != 0

        nbits = 0
        if hasMultTerms:
            nbits = max(nbits, self.calcSB(value.redMultTerm, value.greenMultTerm, value.blueMultTerm))
        if hasAddTerms:
            nbits = max(nbits, self.calcSB(value.redAddTerm, value.greenAddTerm, value.blueAddTerm))

        self.writeUB1(hasAddTerms)
        self.writeUB1(hasMultTerms)
        self.writeUB(4, nbits)

        if hasMultTerms:
            self.writeSB(nbits, value.redMultTerm)
            self.writeSB(nbits, value.greenMultTerm)
            self.writeSB(nbits, value.blueMultTerm)

        if hasAddTerms:
            self.writeSB(nbits, value.redAddTerm)
            self.writeSB(nbits, value.greenAddTerm)
            self.writeSB(nbits, value.blueAddTerm)

        self.align()


    def writeCXFORMWITHALPHA(self, value: ColorTransformWithAlpha) -> None:
        hasMultTerms = value.redMultTerm != 256 and value.greenMultTerm != 256 and value.blueMultTerm != 256 and value.alphaMultTerm != 256
        hasAddTerms = value.redAddTerm != 0 and value.greenAddTerm != 0 and value.blueAddTerm != 0 and value.alphaAddTerm != 0

        nbits = 0
        if hasMultTerms:
            nbits = max(nbits, self.calcSB(value.redMultTerm, value.greenMultTerm, value.blueMultTerm, value.alphaMultTerm))
        if hasAddTerms:
            nbits = max(nbits, self.calcSB(value.redAddTerm, value.greenAddTerm, value.blueAddTerm, value.alphaAddTerm))

        self.writeUB1(hasAddTerms)
        self.writeUB1(hasMultTerms)
        self.writeUB(4, nbits)

        if hasMultTerms:
            self.writeSB(nbits, value.redMultTerm)
            self.writeSB(nbits, value.greenMultTerm)
            self.writeSB(nbits, value.blueMultTerm)
            self.writeSB(nbits, value.alphaMultTerm)

        if hasAddTerms:
            self.writeSB(nbits, value.redAddTerm)
            self.writeSB(nbits, value.greenAddTerm)
            self.writeSB(nbits, value.blueAddTerm)
            self.writeSB(nbits, value.alphaAddTerm)

        self.align()