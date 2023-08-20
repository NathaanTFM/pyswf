from __future__ import annotations
from swf.shapes.FillStyle import FillStyle
from swf.shapes.LineStyle2 import LineStyle2
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.records.Rectangle import Rectangle
from swf.shapes.ShapeWithStyle import ShapeWithStyle

class DefineShape4Tag(Tag):
    """
    DefineShape3 extends the capabilities of DefineShape2
    by extending all of the RGB color fields to support
    RGBA with opacity information.
    """
    tagId = 83

    shapeId: int
    shapeBounds: Rectangle
    edgeBounds: Rectangle
    usesFillWindingRule: bool
    usesNonScalingStrokes: bool
    usesScalingStrokes: bool
    shapes: ShapeWithStyle[FillStyle, LineStyle2]

    def __init__(self, shapeId: int, shapeBounds: Rectangle, edgeBounds: Rectangle, usesFillWindingRule: bool, usesNonScalingStrokes: bool, usesScalingStrokes: bool, shapes: ShapeWithStyle[FillStyle, LineStyle2]) -> None:
        self.shapeId = shapeId
        self.shapeBounds = shapeBounds
        self.edgeBounds = edgeBounds
        self.usesFillWindingRule = usesFillWindingRule
        self.usesNonScalingStrokes = usesNonScalingStrokes
        self.usesScalingStrokes = usesScalingStrokes
        self.shapes = shapes


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")

        shapeId = stream.readUI16()
        shapeBounds = stream.readRECT()
        edgeBounds = stream.readRECT()
        if stream.readUB(5) != 0:
            raise ValueError("reserved is non-zero")

        usesFillWindingRule = bool(stream.readUB(1))
        usesNonScalingStrokes = bool(stream.readUB(1))
        usesScalingStrokes = bool(stream.readUB(1))
        shapes = ShapeWithStyle.read(stream, 4, FillStyle, LineStyle2)

        return DefineShape4Tag(shapeId, shapeBounds, edgeBounds, usesFillWindingRule, usesNonScalingStrokes, usesScalingStrokes, shapes)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        stream.writeUI16(self.shapeId)
        stream.writeRECT(self.shapeBounds)
        stream.writeRECT(self.edgeBounds)
        stream.writeUB(5, 0)
        stream.writeUB(1, self.usesFillWindingRule)
        stream.writeUB(1, self.usesNonScalingStrokes)
        stream.writeUB(1, self.usesScalingStrokes)
        self.shapes.write(stream, 4, FillStyle, LineStyle2)