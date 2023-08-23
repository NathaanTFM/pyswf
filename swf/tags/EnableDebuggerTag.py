from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class EnableDebuggerTag(Tag):
    """
    The EnableDebugger tag enables debugging. The password in the
    EnableDebugger tag is encrypted by using the MD5 algorithm,
    in the same way as the Protect tag.
    """
    tagId = 58

    password: str

    def __init__(self, password: str) -> None:
        self.password = password


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 5:
            raise ValueError("bad swf version")

        password = stream.readString()
        return EnableDebuggerTag(password)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 5:
            raise ValueError("bad swf version")

        stream.writeString(self.password)