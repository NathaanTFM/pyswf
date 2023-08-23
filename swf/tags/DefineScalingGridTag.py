from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.records.Rectangle import Rectangle

class DefineScalingGridTag(Tag):
    """
    The DefineScalingGrid tag introduces the concept of 9-slice scaling,
    which allows component-style scaling to be applied
    to a sprite or button character.
    """
    tagId = 78

    characterId: int
    splitter: Rectangle

    def __init__(self, characterId: int, splitter: Rectangle) -> None:
        self.characterId = characterId
        self.splitter = splitter
        

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 8:
            raise ValueError("bad swf version")
        
        characterId = stream.readUI16()
        splitter = stream.readRECT()
        return DefineScalingGridTag(characterId, splitter)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 8:
            raise ValueError("bad swf version")
        
        stream.writeUI16(self.characterId)
        stream.writeRECT(self.splitter)