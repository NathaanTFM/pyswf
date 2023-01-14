from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class DefineBinaryDataTag(Tag):
    """
    The DefineBinaryData tag permits arbitrary binary data
    to be embedded in a SWF file.
    """
    tagId = 87

    tag: int
    data: bytes

    def __init__(self, tag: int, data: bytes) -> None:
        self.tag = tag
        self.data = data


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 9:
            raise ValueError("bad swf version")

        tag = stream.readUI16()
        
        if stream.readUI32() != 0:
            raise Exception("reserved is non zero")

        data = stream.read(stream.available())
        return DefineBinaryDataTag(tag, data)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 9:
            raise ValueError("bad swf version")

        stream.writeUI16(self.tag)
        stream.writeUI32(0)
        stream.write(self.data)