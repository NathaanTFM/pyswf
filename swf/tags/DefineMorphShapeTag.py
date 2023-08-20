from __future__ import annotations
from swf.shapes.MorphFillStyle import MorphFillStyle
from swf.shapes.MorphLineStyle import MorphLineStyle
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.records.Rectangle import Rectangle
from swf.shapes.Shape import Shape

class DefineMorphShapeTag(Tag):
    """
    The DefineMorphShape tag defines the start and end states
    of a morph sequence. A morph object should be displayed
    with the PlaceObject2 tag, where the ratio field specifies
    how far the morph has progressed.
    """
    tagId = 46

    characterId: int
    startBounds: Rectangle
    endBounds: Rectangle
    morphFillStyles: list[MorphFillStyle]
    morphLineStyles: list[MorphLineStyle]
    startEdges: Shape[MorphFillStyle, MorphLineStyle]
    endEdges: Shape[MorphFillStyle, MorphLineStyle]

    def __init__(self, characterId: int, startBounds: Rectangle, endBounds: Rectangle, morphFillStyles: list[MorphFillStyle], morphLineStyles: list[MorphLineStyle], startEdges: Shape[MorphFillStyle, MorphLineStyle], endEdges: Shape[MorphFillStyle, MorphLineStyle]):
        self.characterId = characterId
        self.startBounds = startBounds
        self.endBounds = endBounds
        self.morphFillStyles = morphFillStyles
        self.morphLineStyles = morphLineStyles
        self.startEdges = startEdges
        self.endEdges = endEdges

    
    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")
        
        characterId = stream.readUI16()
        startBounds = stream.readRECT()
        endBounds = stream.readRECT()
        offset = stream.readUI32()
        morphFillStyles = MorphFillStyle.readArray(stream, 1)
        morphLineStyles = MorphLineStyle.readArray(stream, 1)
        
        startEdges = Shape.read(stream, 1, MorphFillStyle, MorphLineStyle)
        endEdges = Shape.read(stream, 1, MorphFillStyle, MorphLineStyle)

        return DefineMorphShapeTag(characterId, startBounds, endBounds, morphFillStyles, morphLineStyles, startEdges, endEdges)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        # calc this
        numFillBits = stream.calcUB(len(self.morphFillStyles))
        numLineBits = stream.calcUB(len(self.morphLineStyles))

        # write this first (so we can get offset)
        strm2 = SWFOutputStream(stream.version)
        MorphFillStyle.writeArray(strm2, self.morphFillStyles, 1)
        MorphLineStyle.writeArray(strm2, self.morphLineStyles, 1)

        self.startEdges.write(strm2, 1, numFillBits, numLineBits, MorphFillStyle, MorphLineStyle)
        offset = strm2.getLength()
        self.endEdges.write(strm2, 1, numFillBits, numLineBits, MorphFillStyle, MorphLineStyle)

        # begin writing
        stream.writeUI16(self.characterId)
        stream.writeRECT(self.startBounds)
        stream.writeRECT(self.endBounds)
        stream.writeUI32(offset)
        stream.write(strm2.getBytes())