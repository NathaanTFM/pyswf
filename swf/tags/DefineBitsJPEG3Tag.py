from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
import zlib

class DefineBitsJPEG3Tag(Tag):
    """
    This tag defines a bitmap character with JPEG compression.
    This tag extends DefineBitsJPEG2, adding alpha channel (opacity) data.
    """
    tagId = 35

    characterId: int
    imageData: bytes
    bitmapAlphaData: bytes

    def __init__(self, characterId: int, imageData: bytes, bitmapAlphaData: bytes):
        self.characterId = characterId
        self.imageData = imageData
        self.bitmapAlphaData = bitmapAlphaData


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")

        characterId = stream.readUI16()
        alphaDataOffset = stream.readUI32()
        imageData = stream.read(alphaDataOffset)
        bitmapAlphaData = zlib.decompress(stream.read(stream.available()))
        return DefineBitsJPEG3Tag(characterId, imageData, bitmapAlphaData)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        stream.writeUI16(self.characterId)
        stream.writeUI32(len(self.imageData))
        stream.write(self.imageData)
        stream.write(zlib.compress(self.bitmapAlphaData))