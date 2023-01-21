from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class DefineBitsTag(Tag):
    """
    This tag defines a bitmap character with JPEG compression.
    """
    tagId = 6

    characterId: int
    jpegData: bytes

    def __init__(self, characterId: int, jpegData: bytes):
        self.characterId = characterId
        self.jpegData = jpegData

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")

        characterId = stream.readUI16()
        jpegData = stream.read(stream.available())
        return DefineBitsTag(characterId, jpegData)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")

        stream.writeUI16(self.characterId)
        stream.write(self.jpegData)