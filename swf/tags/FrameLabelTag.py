from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class FrameLabelTag(Tag):
    """
    The FrameLabel tag gives the specified Name
    to the current frame.
    """
    tagId = 43

    name: str
    namedAnchor: bool

    def __init__(self, name: str, namedAnchor: bool = False) -> None:
        self.name = name
        self.namedAnchor = namedAnchor


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")

        name = stream.readString()
        namedAnchor = False
        if stream.available():
            if stream.readUI8() != 1:
                raise ValueError("namedanchor set but not 1")
            
            namedAnchor = True

        return FrameLabelTag(name, namedAnchor)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        stream.writeString(self.name)
        if self.namedAnchor:
            stream.writeUI8(1)