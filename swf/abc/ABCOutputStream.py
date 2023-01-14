from __future__ import annotations
import struct


class ABCOutputStream:
    def __init__(self) -> None:
        self.__data = bytearray()


    def length(self) -> int:
        return len(self.__data)


    def getBytes(self) -> bytes:
        return bytes(self.__data)

    
    def write(self, data: bytes, position: int = -1) -> None:
        if position < 0:
            self.__data.extend(data)

        else:
            if position + len(data) > len(self.__data):
                raise Exception("Can't add bytes when rewriting")

            self.__data[position:position+len(data)] = data



    def writeU8(self, value: int, position: int = -1) -> None:
        self.write(struct.pack("<B", value), position)


    def writeU16(self, value: int, position: int = -1) -> None:
        self.write(struct.pack("<H", value), position)


    def writeS24(self, value: int, position: int = -1) -> None:
        assert -0x800000 <= value <= 0x7FFFFF
        if value < 0:
            value += (1 << 24)

        self.writeU8(value & 0xFF, position)
        self.writeU8((value >> 8) & 0xFF, position + 1 if position != -1 else -1)
        self.writeU8((value >> 16) & 0xFF, position + 2 if position != -1 else -1)


    def writeU30(self, value: int) -> None:
        assert 0 <= value <= 0xFFFFFFFF

        while True:
            byte = value & 0x7F
            value >>= 7

            self.writeU8(byte | (0x80 if value else 0))
            if not value:
                break


    def writeU32(self, value: int) -> None:
        self.writeU30(value)

        
    def writeS32(self, value: int) -> None:
        if value < 0:
            value += (1 << 32)

        self.writeU30(value)


    def writeD64(self, value: float, position: int = -1) -> None:
        self.write(struct.pack("<d", value), position)


    def writeS8(self, value: int, position: int = -1) -> None:
        self.write(struct.pack("<b", value), position)


    def writeS16(self, value: int, position: int = -1) -> None:
        self.write(struct.pack("<h", value), position)