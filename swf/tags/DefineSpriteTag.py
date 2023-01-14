from __future__ import annotations
from swf.stream import TagStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class DefineSpriteTag(Tag):
    """
    The DefineSprite tag defines a sprite character.
    """
    tagId = 39

    spriteId: int
    frameCount: int
    controlTags: list[Tag]

    def __init__(self, spriteId: int, frameCount: int, controlTags: list[Tag]) -> None:
        self.spriteId = spriteId
        self.frameCount = frameCount
        self.controlTags = controlTags


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")

        spriteId = stream.readUI16()
        frameCount = stream.readUI16()
        controlTags = []
        while stream.available():
            controlTags.append(TagStream.TagStream.readTag(stream))

        return DefineSpriteTag(spriteId, frameCount, controlTags)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        stream.writeUI16(self.spriteId)
        stream.writeUI16(self.frameCount)
        for tag in self.controlTags:
            TagStream.TagStream.writeTag(stream, tag)