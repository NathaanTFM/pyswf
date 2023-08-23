from __future__ import annotations
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class GlyphEntry:
    glyphIndex: int
    glyphAdvance: int

    def __init__(self, glyphIndex: int, glyphAdvance: int) -> None:
        self.glyphIndex = glyphIndex
        self.glyphAdvance = glyphAdvance


    @staticmethod
    def read(stream: SWFInputStream, glyphBits: int, advanceBits: int) -> GlyphEntry:
        glyphIndex = stream.readUB(glyphBits)
        glyphAdvance = stream.readSB(advanceBits)
        return GlyphEntry(glyphIndex, glyphAdvance)
    

    def write(self, stream: SWFOutputStream, glyphBits: int, advanceBits: int) -> None:
        stream.writeUB(glyphBits, self.glyphIndex)
        stream.writeSB(advanceBits, self.glyphAdvance)