from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag

class RawTag(Tag):
    def __init__(self, tagId: int, data: bytes):
        self.tagId = tagId # type: ignore
        self.data = data


    def write(self, stream: SWFOutputStream) -> None:
        stream.write(self.data)