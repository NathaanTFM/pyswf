from __future__ import annotations
from swf.shapes.FillStyle import FillStyle
from swf.shapes.LineStyle import LineStyle
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.records.Rectangle import Rectangle
from swf.shapes.ShapeWithStyle import ShapeWithStyle

class DefineShapeTag(Tag):
    """
    The DefineShape tag defines a shape for later use
    by control tags such as PlaceObject.
    """
    tagId = 2

    shapeId: int
    shapeBounds: Rectangle
    shapes: ShapeWithStyle[FillStyle, LineStyle]

    def __init__(self, shapeId: int, shapeBounds: Rectangle, shapes: ShapeWithStyle[FillStyle, LineStyle]) -> None:
        self.shapeId = shapeId
        self.shapeBounds = shapeBounds
        self.shapes = shapes


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")

        shapeId = stream.readUI16()
        shapeBounds = stream.readRECT()
        shapes = ShapeWithStyle.read(stream, 1, FillStyle, LineStyle)
        return DefineShapeTag(shapeId, shapeBounds, shapes)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")

        stream.writeUI16(self.shapeId)
        stream.writeRECT(self.shapeBounds)
        self.shapes.write(stream, 1, FillStyle, LineStyle)