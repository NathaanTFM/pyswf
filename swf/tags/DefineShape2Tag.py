from __future__ import annotations
from swf.shapes.FillStyle import FillStyle
from swf.shapes.LineStyle import LineStyle
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.records.Rectangle import Rectangle
from swf.shapes.ShapeWithStyle import ShapeWithStyle

class DefineShape2Tag(Tag):
    """
    DefineShape2 extends the capabilities of DefineShape
    with the ability to support more than 255 styles in
    the style list and multiple style lists in a single
    shape.
    """
    tagId = 22

    shapeId: int
    shapeBounds: Rectangle
    shapes: ShapeWithStyle[FillStyle, LineStyle]

    def __init__(self, shapeId: int, shapeBounds: Rectangle, shapes: ShapeWithStyle[FillStyle, LineStyle]) -> None:
        self.shapeId = shapeId
        self.shapeBounds = shapeBounds
        self.shapes = shapes


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 2:
            raise ValueError("bad swf version")

        shapeId = stream.readUI16()
        shapeBounds = stream.readRECT()
        shapes = ShapeWithStyle.read(stream, 2, FillStyle, LineStyle)
        return DefineShape2Tag(shapeId, shapeBounds, shapes)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 2:
            raise ValueError("bad swf version")

        stream.writeUI16(self.shapeId)
        stream.writeRECT(self.shapeBounds)
        self.shapes.write(stream, 2, FillStyle, LineStyle)