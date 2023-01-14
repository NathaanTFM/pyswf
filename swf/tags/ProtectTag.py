from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

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


    def export(self, stream: SWFInputStream) -> None:
        if stream.version < 2:
            raise ValueError("bad swf version")