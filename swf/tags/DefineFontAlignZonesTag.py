from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class DefineFontAlignZonesTag(Tag):
    """
    The ShowFrame tag instructs Flash Player to display the
    contents of the display list. The file is paused for
    the duration of a single frame.
    """
    tagId = 73

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")
        
        raise NotImplementedError()


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")
        
        raise NotImplementedError()