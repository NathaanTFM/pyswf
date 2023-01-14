from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class RemoveObject2Tag(Tag):
    """
    The RemoveObject2 tag removes the character
    at the specified depth from the display list.
    """
    tagId = 28

    depth: int
    
    def __init__(self, depth: int) -> None:
        self.depth = depth
        

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")

        depth = stream.readUI16()
        return RemoveObject2Tag(depth)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        stream.writeUI16(self.depth)