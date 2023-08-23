from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class DefineFontNameTag(Tag):
    """
    The DefineFontName tag contains the name and copyright information
    for a font embedded in the SWF file.
    """
    tagId = 88

    fontId: int
    fontName: str
    fontCopyright: str

    def __init__(self, fontId: int, fontName: str, fontCopyright: str) -> None:
        self.fontId = fontId
        self.fontName = fontName
        self.fontCopyright = fontCopyright


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 9:
            raise ValueError("bad swf version")
        
        fontId = stream.readUI16()
        fontName = stream.readString()
        fontCopyright = stream.readString()
        return DefineFontNameTag(fontId, fontName, fontCopyright)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 9:
            raise ValueError("bad swf version")
        
        stream.writeUI16(self.fontId)
        stream.writeString(self.fontName)
        stream.writeString(self.fontCopyright)