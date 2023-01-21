from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class JPEGTablesTag(Tag):
    """
    The ShowFrame tag instructs Flash Player to display the
    contents of the display list. The file is paused for
    the duration of a single frame.
    """
    tagId = 8

    jpegData: bytes

    def __init__(self, jpegData: bytes):
        self.jpegData = jpegData


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")

        jpegData = stream.read(stream.available())
        return JPEGTablesTag(jpegData)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")

        stream.write(self.jpegData)