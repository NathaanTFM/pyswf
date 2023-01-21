from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class DefineBitsJPEG2Tag(Tag):
    """
    This tag defines a bitmap character with JPEG compression
    """
    tagId = 21

    characterId: int
    imageData: bytes

    def __init__(self, characterId: int, imageData: bytes):
        self.characterId = characterId
        self.imageData = imageData


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 2:
            raise ValueError("bad swf version")

        characterId = stream.readUI16()
        imageData = stream.read(stream.available())
        return DefineBitsJPEG2Tag(characterId, imageData)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 2:
            raise ValueError("bad swf version")

        stream.writeUI16(self.characterId)
        stream.write(self.imageData)