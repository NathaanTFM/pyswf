from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
import zlib

class DefineBitsJPEG4Tag(Tag):
    """
    This tag defines a bitmap character with JPEG compression.
    This tag extends DefineBitsJPEG3, adding a deblocking parameter.
    """
    tagId = 90

    characterId: int
    deblockParam: int
    imageData: bytes
    bitmapAlphaData: bytes

    def __init__(self, characterId: int, deblockParam: int, imageData: bytes, bitmapAlphaData: bytes):
        self.characterId = characterId
        self.deblockParam = deblockParam
        self.imageData = imageData
        self.bitmapAlphaData = bitmapAlphaData


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 10:
            raise ValueError("bad swf version")

        characterId = stream.readUI16()
        alphaDataOffset = stream.readUI32()
        deblockParam = stream.readUI16()
        imageData = stream.read(alphaDataOffset)
        bitmapAlphaData = zlib.decompress(stream.read(stream.available()))
        return DefineBitsJPEG4Tag(characterId, deblockParam, imageData, bitmapAlphaData)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 10:
            raise ValueError("bad swf version")

        stream.writeUI16(self.characterId)
        stream.writeUI32(len(self.imageData))
        stream.writeUI16(self.deblockParam)
        stream.write(self.imageData)
        stream.write(zlib.compress(self.bitmapAlphaData))