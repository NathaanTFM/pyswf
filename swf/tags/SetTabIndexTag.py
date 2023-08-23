from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class SetTabIndexTag(Tag):
    """
    The SetTabIndex tag sets the index of an object
    within the tab order.
    """
    tagId = 66

    depth: int
    tabIndex: int

    def __init__(self, depth: int, tabIndex: int) -> None:
        self.depth = depth
        self.tabIndex = tabIndex


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 7:
            raise ValueError("bad swf version")
        
        depth = stream.readUI16()
        tabIndex = stream.readUI16()
        return SetTabIndexTag(depth, tabIndex)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 7:
            raise ValueError("bad swf version")
        
        stream.writeUI16(self.depth)
        stream.writeUI16(self.tabIndex)