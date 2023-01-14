from __future__ import annotations
import struct


class ABCInputStream:
    def __init__(self, data: bytes = b"") -> None:
        self.__data = bytearray(data)
        self.__position = 0


    def available(self) -> int:
        return len(self.__data) - self.__position


    def position(self) -> int:
        return self.__position

    
    def peek(self, length: int) -> bytes:
        res = bytes(self.__data[self.__position:self.__position+length])
        if len(res) != length:
            raise EOFError()

        return res

    
    def read(self, length: int) -> bytes:
        res = bytes(self.__data[self.__position:self.__position+length])
        if len(res) != length:
            raise EOFError()

        self.__position += length
        return res


    def skip(self, length: int) -> None:
        if self.__position + length >= len(self.__data):
            raise EOFError()
        
        self.__position += length


    def readU8(self) -> int:
        return struct.unpack("<B", self.read(1))[0] # type: ignore


    def readU16(self) -> int:
        return struct.unpack("<H", self.read(2))[0] # type: ignore


    def readS24(self) -> int:
        value = self.readU8()
        value |= (self.readU8() << 8)
        value |= (self.readU8() << 16)

        if value & (1 << 23):
            value -= (1 << 24)

        return value


    def readU30(self) -> int:
        value = 0
        for n in range(5):
            byte = self.readU8()
            value |= (byte & 0x7F) << (7*n)
            if byte & 0x80 == 0:
                break
            
        return value


    def readU32(self) -> int:
        return self.readU30()

        
    def readS32(self) -> int:
        value = self.readU30()

        if value & (1 << 31):
            value -= (1 << 32)

        return value


    def readD64(self) -> float:
        return struct.unpack("<d", self.read(8))[0] # type: ignore


    def readS8(self) -> int:
        return struct.unpack("<b", self.read(1))[0] # type: ignore


    def readS16(self) -> int:
        return struct.unpack("<h", self.read(2))[0] # type: ignore