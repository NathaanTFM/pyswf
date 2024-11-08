from __future__ import annotations
from swf.shapes.MorphFillStyle import MorphFillStyle
from swf.shapes.MorphLineStyle2 import MorphLineStyle2
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.records.Rectangle import Rectangle
from swf.shapes.Shape import Shape

class DefineMorphShape2Tag(Tag):
    """
    The DefineMorphShape2 tag extends the capabilities of
    DefineMorphShape by using a new morph line style record
    in the morph shape. MORPHLINESTYLE2 allows the use of
    new types of joins and caps as well as scaling options
    and the ability to fill the strokes of the morph shape
    """
    tagId = 84

    characterId: int
    startBounds: Rectangle
    endBounds: Rectangle
    startEdgeBounds: Rectangle
    endEdgeBounds: Rectangle
    usesNonScalingStrokes: bool
    usesScalingStrokes: bool
    morphFillStyles: list[MorphFillStyle]
    morphLineStyles: list[MorphLineStyle2]
    startEdges: Shape[MorphFillStyle, MorphLineStyle2]
    endEdges: Shape[MorphFillStyle, MorphLineStyle2]

    def __init__(self, characterId: int, startBounds: Rectangle, endBounds: Rectangle, startEdgeBounds: Rectangle, endEdgeBounds: Rectangle, usesNonScalingStrokes: bool, usesScalingStrokes: bool, morphFillStyles: list[MorphFillStyle], morphLineStyles: list[MorphLineStyle2], startEdges: Shape[MorphFillStyle, MorphLineStyle2], endEdges: Shape[MorphFillStyle, MorphLineStyle2]):
        self.characterId = characterId
        self.startBounds = startBounds
        self.endBounds = endBounds
        self.startEdgeBounds = startEdgeBounds
        self.endEdgeBounds = endEdgeBounds
        self.usesNonScalingStrokes = usesNonScalingStrokes
        self.usesScalingStrokes = usesScalingStrokes
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
        startEdgeBounds = stream.readRECT()
        endEdgeBounds = stream.readRECT()

        if stream.readUB(6) != 0:
            raise Exception("reserved is non-zero")
        
        usesNonScalingStrokes = stream.readUB1()
        usesScalingStrokes = stream.readUB1()

        offset = stream.readUI32()
        morphFillStyles = MorphFillStyle.readArray(stream, 1)
        morphLineStyles = MorphLineStyle2.readArray(stream, 1)
        
        startEdges = Shape.read(stream, 1, MorphFillStyle, MorphLineStyle2)
        endEdges = Shape.read(stream, 1, MorphFillStyle, MorphLineStyle2)

        return DefineMorphShape2Tag(characterId, startBounds, endBounds, startEdgeBounds, endEdgeBounds, usesNonScalingStrokes, usesScalingStrokes, morphFillStyles, morphLineStyles, startEdges, endEdges)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        # calc this
        numFillBits = stream.calcUB(len(self.morphFillStyles))
        numLineBits = stream.calcUB(len(self.morphLineStyles))

        # write this first (so we can get offset)
        strm2 = SWFOutputStream(stream.version)
        MorphFillStyle.writeArray(strm2, self.morphFillStyles, 1)
        MorphLineStyle2.writeArray(strm2, self.morphLineStyles, 1)

        self.startEdges.write(strm2, 1, numFillBits, numLineBits, MorphFillStyle, MorphLineStyle2)
        offset = strm2.getLength()
        self.endEdges.write(strm2, 1, numFillBits, numLineBits, MorphFillStyle, MorphLineStyle2)

        # begin writing
        stream.writeUI16(self.characterId)
        stream.writeRECT(self.startBounds)
        stream.writeRECT(self.endBounds)
        stream.writeRECT(self.startEdgeBounds)
        stream.writeRECT(self.endEdgeBounds)
        stream.writeUB(6, 0)
        stream.writeUB(1, int(self.usesNonScalingStrokes))
        stream.writeUB(1, int(self.usesScalingStrokes))
        stream.writeUI32(offset)
        stream.write(strm2.getBytes())
