from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class EndTag(Tag):
    """
    The End tag marks the end of a file.
    """
    tagId = 0

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")

        return EndTag()
        

    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")