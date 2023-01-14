from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class EnableDebugger2Tag(Tag):
    """
    The EnableDebugger2 tag enables debugging.
    """
    tagId = 64

    reserved: int
    password: str

    def __init__(self, password: str, reserved: int = 0) -> None:
        self.password = password
        self.reserved = reserved


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 6:
            raise ValueError("bad swf version")

        reserved = stream.readUI16()
        password = stream.readString()
        return EnableDebugger2Tag(password, reserved)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 6:
            raise ValueError("bad swf version")

        stream.writeUI16(self.reserved)
        stream.writeString(self.password)