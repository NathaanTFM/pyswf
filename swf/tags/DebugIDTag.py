from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class DebugIDTag(Tag):
    """
    Non-documented SWF tag
    """
    tagId = 41

    uuid: bytes

    def __init__(self, uuid: bytes):
        self.uuid = uuid


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")
    
        uuid = stream.read(stream.available())
        return DebugIDTag(uuid)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        stream.write(self.uuid)