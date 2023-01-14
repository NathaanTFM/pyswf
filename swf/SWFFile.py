from __future__ import annotations
from swf.records.Rectangle import Rectangle
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.enums.Compression import Compression
from swf.stream.TagStream import TagStream
from typing import TypeVar
import struct
import zlib
import lzma
import warnings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.tags.Tag import Tag

    T = TypeVar('T', bound=Tag)

class SWFFile:
    compression: Compression
    version: int

    frameSize: Rectangle
    frameRate: int
    frameCount: int

    tags: list[Tag]

    def __init__(self, swfData: bytes | None = None):
        """
        Initializes a SWF File with dummy values
        If data is passed, the passed swf file is parsed instead.
        """
        if swfData:
            # read the swf header
            compression = Compression(swfData[0])
            if swfData[1] != 87:
                raise Exception("not a swf file")

            if swfData[2] != 83:
                raise Exception("not a swf file")

            self.version = swfData[3]
            fileLength = struct.unpack("<I", swfData[4:8])[0]

            if compression == Compression.ZLIB:
                data = zlib.decompress(swfData[8:])

            elif compression == Compression.LZMA:
                data = lzma.decompress(swfData[8:])

            else:
                data = swfData[8:]

            if len(data) != fileLength-8:
                warnings.warn("swf file length is incorrect")


            # we have got a decompressed swf, read it now
            stream = SWFInputStream(self.version, data)
            self.frameSize = stream.readRECT()
            self.frameRate = stream.readUI16()
            self.frameCount = stream.readUI16()
            
            # read tags
            self.tags = []
            while stream.available():
                tag = TagStream.readTag(stream)
                self.tags.append(tag)

        else:
            self.version = 1
            self.frameSize = Rectangle(0, 0, 0, 0)
            self.frameRate = 30
            self.frameCount = 0
            self.tags = []


    def export(self, compression: Compression) -> bytes:
        """
        Export the SWF to bytes
        """
        stream = SWFOutputStream(self.version)
        stream.writeRECT(self.frameSize)
        stream.writeUI16(self.frameRate)
        stream.writeUI16(self.frameCount)
        
        for tag in self.tags:
            TagStream.writeTag(stream, tag)

        data = stream.getBytes()

        header = struct.pack("<BBBBI", compression.value, 87, 83, self.version, len(data)+8)
        if compression == Compression.ZLIB:
            return header + zlib.compress(data)
        elif compression == Compression.LZMA:
            return header + lzma.compress(data)
        else:
            return header + data


    def findTags(self, type: type[T]) -> list[T]:
        """
        Find every tag with specified type
        """
        res = []
        for tag in self.tags:
            if isinstance(tag, type):
                res.append(tag)

        return res