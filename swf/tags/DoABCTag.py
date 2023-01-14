from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class DoABCTag(Tag):
    """
    The DoABC tag is similar to the DoAction tag: it defines
    a series of bytecodes to be executed.
    """
    tagId = 82

    flags: int
    name: str
    abcData: bytes

    def __init__(self, flags: int, name: str, abcData: bytes) -> None:
        self.flags = flags
        self.name = name
        self.abcData = abcData


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 9:
            raise ValueError("bad swf version")

        flags = stream.readUI32()
        name = stream.readString()
        abcData = stream.read(stream.available())
        return DoABCTag(flags, name, abcData)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 9:
            raise ValueError("bad swf version")

        stream.writeUI32(self.flags)
        stream.writeString(self.name)
        stream.write(self.abcData)