from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ProtectTag(Tag):
    """
    The Protect tag marks a file as not importable
    for editing in an authoring environment.
    """
    tagId = 24

    password: str | None

    def __init__(self, password: str | None = None) -> None:
        self.password = password


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 2:
            raise ValueError("bad swf version")

        password = None
        if stream.available():
            if stream.version < 5:
                raise ValueError("not supported password")

            password = stream.readString()

        return ProtectTag(password)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 2:
            raise ValueError("bad swf version")
        
        if self.password is not None:
            if stream.version < 5:
                raise ValueError("not supported password")
            
            stream.writeString(self.password)