from __future__ import annotations
from swf.records.ColorTransform import ColorTransform
from swf.records.Matrix import Matrix
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class PlaceObjectTag(Tag):
    """
    The PlaceObject tag adds a character to
    the display list.
    """
    tagId = 4

    characterId: int
    depth: int
    matrix: Matrix
    colorTransform: ColorTransform | None

    def __init__(self, characterId: int, depth: int, matrix: Matrix, colorTransform: ColorTransform | None = None):
        self.characterId = characterId
        self.depth = depth
        self.matrix = matrix
        self.colorTransform = colorTransform


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")

        characterId = stream.readUI16()
        depth = stream.readUI16()
        matrix = stream.readMATRIX()
        cxform = None
        if stream.available():
            cxform = stream.readCXFORM()

        return PlaceObjectTag(characterId, depth, matrix, cxform)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")

        stream.writeUI16(self.characterId)
        stream.writeUI16(self.depth)
        stream.writeMATRIX(self.matrix)
        if self.colorTransform:
            stream.writeCXFORM(self.colorTransform)