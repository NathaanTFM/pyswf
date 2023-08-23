from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.records.Rectangle import Rectangle
from swf.records.Matrix import Matrix
from swf.texts.TextRecord import TextRecord
from swf.records.RGBA import RGBA

class DefineText2Tag(Tag):
    """
    The DefineText2 tag is almost identical to the DefineText tag.
    The only difference is that Type 1 text records contained within a DefineText2 tag
    use an RGBA value (rather than an RGB value) to define TextColor.
    This allows partially or completely transparent characters.
    """
    tagId = 33

    characterId: int
    textBounds: Rectangle
    textMatrix: Matrix
    textRecords: list[TextRecord[RGBA]]

    def __init__(self, characterId: int, textBounds: Rectangle, textMatrix: Matrix, textRecords: list[TextRecord[RGBA]]) -> None:
        self.characterId = characterId
        self.textBounds = textBounds
        self.textMatrix = textMatrix
        self.textRecords = textRecords


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")
        
        characterId = stream.readUI16()
        textBounds = stream.readRECT()
        textMatrix = stream.readMATRIX()
        glyphBits = stream.readUI8()
        advanceBits = stream.readUI8()
        textRecords = []
        while 1:
            record: TextRecord[RGBA] | None = TextRecord.read(stream, 2, glyphBits, advanceBits)
            if not record:
                break

            textRecords.append(record)
            
        return DefineText2Tag(characterId, textBounds, textMatrix, textRecords)
    

    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")
        
        glyphBits = stream.calcUB(*[glyph.glyphIndex for record in self.textRecords for glyph in record.glyphEntries])
        advanceBits = stream.calcSB(*[glyph.glyphAdvance for record in self.textRecords for glyph in record.glyphEntries])

        stream.writeUI16(self.characterId)
        stream.writeRECT(self.textBounds)
        stream.writeMATRIX(self.textMatrix)
        stream.writeUI8(glyphBits)
        stream.writeUI8(advanceBits)

        for record in self.textRecords:
            record.write(stream, 2, glyphBits, advanceBits)

        stream.writeUI8(0)