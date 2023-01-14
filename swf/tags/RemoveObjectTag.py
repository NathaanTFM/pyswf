from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class RemoveObjectTag(Tag):
    """
    The RemoveObject tag removes the specified character
    (at the specified depth) from the display list.
    """
    tagId = 5

    characterId: int
    depth: int

    def __init__(self, characterId: int, depth: int) -> None:
        self.characterId = characterId
        self.depth = depth


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")

        characterId = stream.readUI16()
        depth = stream.readUI16()
        return RemoveObjectTag(characterId, depth)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")

        stream.writeUI16(self.characterId)
        stream.writeUI16(self.depth)