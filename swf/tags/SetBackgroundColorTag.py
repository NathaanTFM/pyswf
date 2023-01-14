from __future__ import annotations
from swf.records.RGB import RGB
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class SetBackgroundColorTag(Tag):
    """
    The SetBackgroundColor tag sets the background color
    of the display.
    """
    tagId = 9

    backgroundColor: RGB

    def __init__(self, backgroundColor: RGB) -> None:
        self.backgroundColor = backgroundColor


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")

        backgroundColor = stream.readRGB()
        return SetBackgroundColorTag(backgroundColor)
        

    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")

        stream.writeRGB(self.backgroundColor)