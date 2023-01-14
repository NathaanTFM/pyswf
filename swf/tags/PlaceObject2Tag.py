from __future__ import annotations
from swf.actions.ClipActionRecord import ClipActionRecord
from swf.records.ColorTransformWithAlpha import ColorTransformWithAlpha
from swf.records.Matrix import Matrix
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class PlaceObject2Tag(Tag):
    """
    The PlaceObject2 tag extends the functionality
    of the PlaceObject tag.
    """
    tagId = 26

    move: bool
    depth: int
    characterId: int | None
    matrix: Matrix | None
    colorTransform: ColorTransformWithAlpha | None
    ratio: int | None
    name: str | None
    clipDepth: int | None
    clipActions: list[ClipActionRecord] | None

    def __init__(self, move: bool, depth: int, characterId: int | None = None, matrix: Matrix | None = None, colorTransform: ColorTransformWithAlpha | None = None, ratio: int | None = None, name: str | None = None, clipDepth: int | None = None, clipActions: list[ClipActionRecord] | None = None) -> None:
        self.move = move
        self.depth = depth
        self.characterId = characterId
        self.matrix = matrix
        self.colorTransform = colorTransform
        self.ratio = ratio
        self.name = name
        self.clipDepth = clipDepth
        self.clipActions = clipActions


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")

        hasClipActions = stream.readUB1()
        hasClipDepth = stream.readUB1()
        hasName = stream.readUB1()
        hasRatio = stream.readUB1()
        hasColorTransform = stream.readUB1()
        hasMatrix = stream.readUB1()
        hasCharacter = stream.readUB1()
        move = stream.readUB1()
        
        depth = stream.readUI16()

        characterId = None
        if hasCharacter:
            characterId = stream.readUI16()

        matrix = None
        if hasMatrix:
            matrix = stream.readMATRIX()

        colorTransform = None
        if hasColorTransform:
            colorTransform = stream.readCXFORMWITHALPHA()

        ratio = None
        if hasRatio:
            ratio = stream.readUI16()

        name = None
        if hasName:
            name = stream.readString()

        clipDepth = None
        if hasClipDepth:
            clipDepth = stream.readUI16()

        clipActions = None
        if hasClipActions:
            if stream.version < 5:
                raise ValueError("bad swf version")

            clipActions = ClipActionRecord.readArray(stream)

        return PlaceObject2Tag(move, depth, characterId, matrix, colorTransform, ratio, name, clipDepth, clipActions)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        stream.writeUB1(self.clipActions is not None)
        stream.writeUB1(self.clipDepth is not None)
        stream.writeUB1(self.name is not None)
        stream.writeUB1(self.ratio is not None)
        stream.writeUB1(self.colorTransform is not None)
        stream.writeUB1(self.matrix is not None)
        stream.writeUB1(self.characterId is not None)
        stream.writeUB1(self.move)

        stream.writeUI16(self.depth)

        if self.characterId is not None:
            stream.writeUI16(self.characterId)

        if self.matrix is not None:
            stream.writeMATRIX(self.matrix)

        if self.colorTransform is not None:
            stream.writeCXFORMWITHALPHA(self.colorTransform)

        if self.ratio is not None:
            stream.writeUI16(self.ratio)

        if self.name is not None:
            stream.writeString(self.name)

        if self.clipDepth is not None:
            stream.writeUI16(self.clipDepth)

        if self.clipActions is not None:
            if stream.version < 5:
                raise Exception("bad swf version")

            ClipActionRecord.writeArray(stream, self.clipActions)