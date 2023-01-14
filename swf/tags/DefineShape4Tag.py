from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class DefineShape4Tag(Tag):
    """
    The ShowFrame tag instructs Flash Player to display the
    contents of the display list. The file is paused for
    the duration of a single frame.
    """
    tagId = 83

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")


    def export(self, stream: SWFInputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")