from __future__ import annotations
from swf.actions.ClipActionRecord import ClipActionRecord
from swf.filters.Filter import Filter
from swf.records.ColorTransformWithAlpha import ColorTransformWithAlpha
from swf.records.Matrix import Matrix
from swf.records.RGBA import RGBA
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.enums.BlendMode import BlendMode
from swf.stream.SWFInputStream import SWFInputStream
from swf.tags.PlaceObject3Tag import PlaceObject3Tag

class PlaceObject4Tag(Tag):
    """
    The PlaceObject4 tag extends the functionality of the
    PlaceObject3 tag.
    """
    tagId = 70

    move: bool
    hasImage: bool
    depth: int
    className: str | None
    characterId: int | None
    matrix: Matrix | None
    colorTransform: ColorTransformWithAlpha | None
    ratio: int | None
    name: str | None
    clipDepth: int | None
    surfaceFilterList: list[Filter] | None
    blendMode: BlendMode | None
    bitmapCache: int | None
    visible: int | None
    backgroundColor: RGBA | None
    clipActions: list[ClipActionRecord] | None
    amfData: bytes | None

    # move, hasImage, depth, className, characterId, matrix, colorTransform, ratio, name, clipDepth, surfaceFilterList, blendMode, bitmapCache, visible, backgroundColor, clipActions
    def __init__(self, move: bool, hasImage: bool, depth: int, className: str | None = None, characterId: int | None = None, matrix: Matrix | None = None, colorTransform: ColorTransformWithAlpha | None = None, ratio: int | None = None, name: str | None = None, clipDepth: int | None = None, surfaceFilterList: list[Filter] | None = None, blendMode: BlendMode | None = None, bitmapCache: int | None = None, visible: int | None = None, backgroundColor: RGBA | None = None, clipActions: list[ClipActionRecord] | None = None, amfData: bytes | None = None) -> None:
        self.move = move
        self.hasImage = hasImage
        self.depth = depth
        self.className = className
        self.characterId = characterId
        self.matrix = matrix
        self.colorTransform = colorTransform
        self.ratio = ratio
        self.name = name
        self.clipDepth = clipDepth
        self.surfaceFilterList = surfaceFilterList
        self.blendMode = blendMode
        self.bitmapCache = bitmapCache
        self.visible = visible
        self.backgroundColor = backgroundColor
        self.clipActions = clipActions
        self.amfData = amfData


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        # quick shortcut
        tag = PlaceObject3Tag.read(stream)
        assert type(tag) == PlaceObject3Tag

        amfData = None
        if stream.available():
            amfData = stream.read(stream.available())

        return PlaceObject4Tag(
            tag.move,
            tag.hasImage,
            tag.depth,
            tag.className,
            tag.characterId,
            tag.matrix,
            tag.colorTransform,
            tag.ratio,
            tag.name,
            tag.clipDepth,
            tag.surfaceFilterList,
            tag.blendMode,
            tag.bitmapCache,
            tag.visible,
            tag.backgroundColor,
            tag.clipActions, 
            amfData
        )


    def write(self, stream: SWFOutputStream) -> None:
        # don't mind this: the two classes are compatible, but I don't want to add inheritance
        # because those are clearly two distinct tags
        PlaceObject3Tag.write(self, stream) # type: ignore

        if self.amfData is not None:
            stream.write(self.amfData)