from __future__ import annotations
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.texts.GlyphEntry import GlyphEntry
from swf.records.RGB import RGB
from swf.records.RGBA import RGBA

class TextRecord:
    fontId: int | None
    textColor: RGB | RGBA | None
    xOffset: int | None
    yOffset: int | None
    textHeight: int | None
    glyphEntries: list[GlyphEntry]

    def __init__(self, fontId: int | None, textColor: RGB | RGBA | None, xOffset: int | None, yOffset: int | None, textHeight: int | None, glyphEntries: list[GlyphEntry]) -> None:
        self.fontId = fontId
        self.textColor = textColor
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.textHeight = textHeight
        self.glyphEntries = glyphEntries


    @staticmethod
    def read(stream: SWFInputStream, tag: int, glyphBits: int, advanceBits: int) -> TextRecord | None:
        textRecordType = stream.readUB(1)

        styleFlagsReserved = stream.readUB(3)
        if styleFlagsReserved != 0:
            raise Exception("reserved is non zero")
        
        styleFlagsHasFont = stream.readUB1()
        styleFlagsHasColor = stream.readUB1()
        styleFlagsHasYOffset = stream.readUB1()
        styleFlagsHasXOffset = stream.readUB1()

        # if everything is zero, then we have nothing
        if not (textRecordType or styleFlagsHasFont or styleFlagsHasColor or styleFlagsHasYOffset or styleFlagsHasXOffset):
            return None
        
        if textRecordType != 1:
            raise Exception("textRecordType must be 1")

        fontId = None
        if styleFlagsHasFont:
            fontId = stream.readUI16()

        textColor: RGB | RGBA | None = None
        if styleFlagsHasColor:
            if tag == 2:
                textColor = stream.readRGBA()
            else:
                textColor = stream.readRGB()
        
        xOffset = None
        if styleFlagsHasXOffset:
            xOffset = stream.readSI16()
        
        yOffset = None
        if styleFlagsHasYOffset:
            yOffset = stream.readSI16()

        textHeight = None
        if styleFlagsHasFont:
            textHeight = stream.readUI16()

        glyphCount = stream.readUI8()

        glyphEntries = []
        for _ in range(glyphCount):
            entry = GlyphEntry.read(stream, glyphBits, advanceBits)
            glyphEntries.append(entry)

        stream.align()
        return TextRecord(fontId, textColor, xOffset, yOffset, textHeight, glyphEntries)
    

    def write(self, stream: SWFOutputStream, tag: int, glyphBits: int, advanceBits: int) -> None:
        if (self.fontId is not None) != (self.textHeight is not None):
            raise Exception("both fontId and textHeight must be (un)set")
        
        stream.writeUB(1, 1)
        stream.writeUB(3, 0)
        stream.writeUB1(self.fontId is not None)
        stream.writeUB1(self.textColor is not None)
        stream.writeUB1(self.yOffset is not None)
        stream.writeUB1(self.xOffset is not None)

        if self.fontId is not None:
            stream.writeUI16(self.fontId)

        if self.textColor is not None:
            if tag == 1:
                if type(self.textColor) != RGB:
                    raise Exception("expected RGB for textColor")
                
                stream.writeRGB(self.textColor)

            elif tag == 2:
                if type(self.textColor) != RGBA:
                    raise Exception("expected RGBA for textColor")
                
                stream.writeRGBA(self.textColor)

        if self.xOffset is not None:
            stream.writeSI16(self.xOffset)

        if self.yOffset is not None:
            stream.writeSI16(self.yOffset)

        if self.textHeight is not None:
            stream.writeUI16(self.textHeight)

        stream.writeUI8(len(self.glyphEntries))
        for entry in self.glyphEntries:
            entry.write(stream, glyphBits, advanceBits)

        stream.align()