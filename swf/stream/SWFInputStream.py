from __future__ import annotations
from typing import Any
from swf.enums.LanguageCode import LanguageCode
from swf.records.RGB import RGB
from swf.records.RGBA import RGBA
from swf.records.Rectangle import Rectangle
from swf.records.Matrix import Matrix
from swf.records.ColorTransform import ColorTransform
from swf.records.ColorTransformWithAlpha import ColorTransformWithAlpha
from swf.Debugging import Debugging
import struct


class SWFInputStream:
    if Debugging.enableStreamVerbose():
        debugBuffer: str = ""

    version: int

    def __init__(self, version: int, data: bytes) -> None:
        self.version = version
        self.__data = bytearray(data)
        self.__position = 0
        self.__bitposition = 0

        # are we in hyper ultra mega verbose mode?
        if Debugging.enableStreamVerbose():
            import os, inspect
            def verbosefunc(func: Any) -> Any:
                def tmpfunc(*args: Any, **kwargs: Any) -> Any:
                    ret = func(*args, **kwargs)

                    caller = inspect.stack()[1]
                    filename = os.path.basename(caller.filename)

                    # most recent caller is SWFInputStream, give up
                    if filename != "SWFInputStream.py":
                        SWFInputStream.debugBuffer += (filename + ":" + str(caller.lineno) + " -> " + str(func.__name__) + repr(args) + " = " + repr(ret)) + "\n"

                    return ret
                
                return tmpfunc
            
            import types
            for name in dir(self):
                value = getattr(self, name)
                if name.startswith("read") and isinstance(value, types.MethodType):
                    setattr(self, name, verbosefunc(value))


    def available(self) -> int:
        """
        Returns the number of available bytes
        """
        assert self.__bitposition == 0
        return len(self.__data) - self.__position

    
    def peek(self, length: int) -> bytes:
        """
        Peek n bytes from the buffer at current position
        """
        assert self.__bitposition == 0
        res = bytes(self.__data[self.__position:self.__position+length])
        if len(res) != length:
            raise EOFError()

        return res

    
    def read(self, length: int) -> bytes:
        """
        Read n bytes from the buffer at current position
        """
        assert self.__bitposition == 0
        res = bytes(self.__data[self.__position:self.__position+length])
        if len(res) != length:
            raise EOFError()

        self.__position += length
        return res


    def skip(self, length: int) -> None:
        """
        Skip n bytes from the buffer
        """
        assert self.__bitposition == 0
        if self.__position + length > len(self.__data):
            raise EOFError()
        
        self.__position += length


    def readSI8(self) -> int:
        """
        Read a signed 8 bit integer value at current position
        """
        return struct.unpack("<b", self.read(1))[0] # type: ignore


    def readSI16(self) -> int:
        """
        Read a signed 16 bit integer value at current position
        """
        return struct.unpack("<h", self.read(2))[0] # type: ignore


    def readSI32(self) -> int:
        """
        Read a signed 16 bit integer value at current position
        """
        return struct.unpack("<i", self.read(4))[0] # type: ignore


    def readUI8(self) -> int:
        """
        Read an unsigned 8 bit integer value at current position
        """
        return struct.unpack("<B", self.read(1))[0] # type: ignore


    def readUI16(self) -> int:
        """
        Read an unsigned 16 bit integer value at current position
        """
        return struct.unpack("<H", self.read(2))[0] # type: ignore


    def readUI32(self) -> int:
        """
        Read an unsigned 32 bit integer value at current position
        """
        return struct.unpack("<I", self.read(4))[0] # type: ignore


    def readUI64(self) -> int:
        """
        Read an unsigned 64 bit integer value at current position
        """
        return struct.unpack("<Q", self.read(8))[0] # type: ignore


    def readFIXED(self) -> float:
        """
        Read a 32-bit 16.16 fixed-point number at current position
        """
        return self.readUI32() / 65536


    def readFIXED8(self) -> float:
        """
        Read a 16-bit 8.8 fixed-point number at current position
        """
        return self.readUI16() / 256


    def readFLOAT16(self) -> float:
        """
        Read a half-precision (16-bit) floating-point number
        """
        value = self.readUI16()
        if value == 0:
            return 0

        sign = (-1 if value & 0x8000 else 1)
        exponent = ((value >> 10) & 0x1F) - 16
        mantissa = 1 + (value & 0x3FF) / 0x400

        return sign * (2**exponent) * mantissa # type: ignore

    
    def readFLOAT(self) -> float:
        """
        Read a single-precision (32-bit) floating-point number
        """
        return struct.unpack("<f", self.read(4))[0] # type: ignore

    
    def readDOUBLE(self) -> float:
        """
        Read a double-precision (64-bit) floating-point number
        """
        assert self.__bitposition == 0
        return struct.unpack("<d", self.read(8))[0] # type: ignore


    def readEncodedU32(self) -> int:
        """
        Read a variable length encoded 32-bit unsigned integer
        """
        value = 0
        for n in range(5):
            byte = self.readUI8()
            value |= (byte & 0x7F) << (7*n)
            if byte & 0x80 == 0:
                break
            
        return value


    def readUB(self, length: int) -> int:
        """
        Read an unsigned-bit value
        """
        if length == 0:
            return 0

        value = 0
        while length:
            avail = 8 - self.__bitposition
            if length >= avail:
                length -= avail
                value |= (self.__data[self.__position] & ((1 << avail) - 1)) << length
                self.__bitposition = 0
                self.__position += 1

            else:
                value |= (self.__data[self.__position] >> (avail - length)) & ((1 << length) - 1)
                self.__bitposition += length
                break

        return value


    def readSB(self, length: int) -> int:
        """
        Read a signed-bit value
        """
        if length == 0:
            return 0

        value = self.readUB(length)
        if value >> (length - 1):
            value -= (1 << length)
        
        return value


    def readFB(self, length: int) -> float:
        """
        Read a signed, fixed-point bit value
        """
        if length == 0:
            return 0.0

        return self.readSB(length) / 65536


    def readUB1(self) -> bool:
        """
        Read a single bit as a boolean value
        """
        return bool(self.readUB(1))


    def align(self) -> None:
        """
        Align to the next byte
        """
        if self.__bitposition:
            self.__bitposition = 0
            self.__position += 1


    def readString(self) -> str:
        """
        Read a string value
        """
        index = self.__data.find(0, self.__position)
        if index == -1:
            raise EOFError()

        value = self.__data[self.__position:index]
        self.__position = index+1
        
        if self.version >= 6:
            return value.decode("utf8")
        else:
            return value.decode("ansi") # assume ansi, could be shift-JIS


    def readLanguageCode(self) -> LanguageCode:
        """
        Read a language code
        """
        return LanguageCode(self.readUI8())


    def readRGB(self) -> RGB:
        """
        Read a RGB record
        """
        red = self.readUI8()
        green = self.readUI8()
        blue = self.readUI8()
        return RGB(red, green, blue)


    def readRGBA(self) -> RGBA:
        """
        Read a RGBA record
        """
        red = self.readUI8()
        green = self.readUI8()
        blue = self.readUI8()
        alpha = self.readUI8()
        return RGBA(red, green, blue, alpha)


    def readARGB(self) -> RGBA:
        """
        Read an ARGB record
        """
        alpha = self.readUI8()
        red = self.readUI8()
        green = self.readUI8()
        blue = self.readUI8()
        return RGBA(red, green, blue, alpha)


    def readRECT(self) -> Rectangle:
        """
        Read a RECT record
        """
        nbits = self.readUB(5)
        xMin = self.readSB(nbits)
        xMax = self.readSB(nbits)
        yMin = self.readSB(nbits)
        yMax = self.readSB(nbits)
        self.align()
        return Rectangle(xMin, xMax, yMin, yMax)


    def readMATRIX(self) -> Matrix:
        """
        Read a MATRIX record
        """
        scaleX, scaleY = 1.0, 1.0
        hasScale = self.readUB1()
        if hasScale:
            nScaleBits = self.readUB(5)
            scaleX = self.readFB(nScaleBits)
            scaleY = self.readFB(nScaleBits)

        rotateSkew0, rotateSkew1 = 0.0, 0.0
        hasRotate = self.readUB1()
        if hasRotate:
            nRotateBits = self.readUB(5)
            rotateSkew0 = self.readFB(nRotateBits)
            rotateSkew1 = self.readFB(nRotateBits)

        nTranslateBits = self.readUB(5)
        translateX = self.readSB(nTranslateBits)
        translateY = self.readSB(nTranslateBits)
        self.align()
        
        mat = Matrix(translateX, translateY, scaleX=scaleX, scaleY=scaleY, rotateSkew0=rotateSkew0, rotateSkew1=rotateSkew1)
        return mat


    def readCXFORM(self) -> ColorTransform:
        """
        Read a CXFORM record
        """
        cxform = ColorTransform()

        hasAddTerms = self.readUB1()
        hasMultTerms = self.readUB1()
        nbits = self.readUB(4)

        if hasMultTerms:
            cxform.redMultTerm = self.readSB(nbits)
            cxform.greenMultTerm = self.readSB(nbits)
            cxform.blueMultTerm = self.readSB(nbits)

        if hasAddTerms:
            cxform.redAddTerm = self.readSB(nbits)
            cxform.greenAddTerm = self.readSB(nbits)
            cxform.blueAddTerm = self.readSB(nbits)

        self.align()
        return cxform


    def readCXFORMWITHALPHA(self) -> ColorTransformWithAlpha:
        """
        Read a CXFORM record
        """
        cxform = ColorTransformWithAlpha()

        hasAddTerms = self.readUB1()
        hasMultTerms = self.readUB1()
        nbits = self.readUB(4)

        if hasMultTerms:
            cxform.redMultTerm = self.readSB(nbits)
            cxform.greenMultTerm = self.readSB(nbits)
            cxform.blueMultTerm = self.readSB(nbits)
            cxform.alphaMultTerm = self.readSB(nbits)

        if hasAddTerms:
            cxform.redAddTerm = self.readSB(nbits)
            cxform.greenAddTerm = self.readSB(nbits)
            cxform.blueAddTerm = self.readSB(nbits)
            cxform.alphaAddTerm = self.readSB(nbits)

        self.align()
        return cxform