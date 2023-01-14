from __future__ import annotations
from swf.actions.ClipActionRecord import ClipActionRecord
from swf.filters.Filter import Filter
from swf.filters.FilterList import FilterList
from swf.records.ColorTransform import ColorTransform
from swf.records.ColorTransformWithAlpha import ColorTransformWithAlpha
from swf.records.Matrix import Matrix
from swf.records.RGBA import RGBA
from swf.records.Rectangle import Rectangle
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.enums.BlendMode import BlendMode
from swf.stream.SWFInputStream import SWFInputStream

class PlaceObject3Tag(Tag):
    """
    The PlaceObject3 tag extends the functionality of the
    PlaceObject2 tag.
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

    # move, hasImage, depth, className, characterId, matrix, colorTransform, ratio, name, clipDepth, surfaceFilterList, blendMode, bitmapCache, visible, backgroundColor, clipActions
    def __init__(self, move: bool, hasImage: bool, depth: int, className: str | None = None, characterId: int | None = None, matrix: Matrix | None = None, colorTransform: ColorTransformWithAlpha | None = None, ratio: int | None = None, name: str | None = None, clipDepth: int | None = None, surfaceFilterList: list[Filter] | None = None, blendMode: BlendMode | None = None, bitmapCache: int | None = None, visible: int | None = None, backgroundColor: RGBA | None = None, clipActions: list[ClipActionRecord] | None = None) -> None:
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


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 8:
            raise ValueError("bad swf version")

        hasClipActions = stream.readUB1()
        hasClipDepth = stream.readUB1()
        hasName = stream.readUB1()
        hasRatio = stream.readUB1()
        hasColorTransform = stream.readUB1()
        hasMatrix = stream.readUB1()
        hasCharacter = stream.readUB1()
        move = stream.readUB1()

        if stream.readUB(1) != 0:
            raise Exception("reserved is set")

        opaqueBackground = stream.readUB1()
        hasVisible = stream.readUB1()
        hasImage = stream.readUB1()
        hasClassName = stream.readUB1()
        hasCacheAsBitmap = stream.readUB1()
        hasBlendMode = stream.readUB1()
        hasFilterList = stream.readUB1()

        depth = stream.readUI16()

        # hasClassName or (hasImage and hasCharacter)
        className = None
        if hasClassName:
            className = stream.readString()

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

        surfaceFilterList = None
        if hasFilterList:
            surfaceFilterList = []

            numberOfFilters = stream.readUI8()
            for _ in range(numberOfFilters):
                filterId = stream.readUI8()
                filter = FilterList[filterId].read(stream)
                surfaceFilterList.append(filter)

        blendMode = None
        if hasBlendMode:
            blendMode = BlendMode(stream.readUI8())

        bitmapCache = None
        if hasCacheAsBitmap:
            bitmapCache = stream.readUI8()

        visible = None
        if hasVisible:
            visible = stream.readUI8()
            if visible > 1:
                raise ValueError("bad value for visible")

        backgroundColor = None
        if opaqueBackground:
            backgroundColor = stream.readRGBA()

        clipActions = None
        if hasClipActions:
            clipActions = ClipActionRecord.readArray(stream)

        return PlaceObject3Tag(move, hasImage, depth, className, characterId, matrix, colorTransform, ratio, name, clipDepth, surfaceFilterList, blendMode, bitmapCache, visible, backgroundColor, clipActions)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 8:
            raise ValueError("bad swf version")

        stream.writeUB1(self.clipActions is not None)
        stream.writeUB1(self.clipDepth is not None)
        stream.writeUB1(self.name is not None)
        stream.writeUB1(self.ratio is not None)
        stream.writeUB1(self.colorTransform is not None)
        stream.writeUB1(self.matrix is not None)
        stream.writeUB1(self.characterId is not None)
        stream.writeUB1(self.move)

        stream.writeUB(1, 0)
        stream.writeUB1(self.backgroundColor is not None)
        stream.writeUB1(self.visible is not None)
        stream.writeUB1(self.hasImage)
        stream.writeUB1(self.className is not None)
        stream.writeUB1(self.bitmapCache is not None)
        stream.writeUB1(self.blendMode is not None)
        stream.writeUB1(self.surfaceFilterList is not None)

        stream.writeUI16(self.depth)

        if self.className is not None:
            stream.writeString(self.className)

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

        if self.surfaceFilterList is not None:
            stream.writeUI8(len(self.surfaceFilterList))
            for filter in self.surfaceFilterList:
                stream.writeUI8(filter.id)
                filter.write(stream)

        if self.blendMode is not None:
            stream.writeUI8(self.blendMode.value)

        if self.bitmapCache is not None:
            stream.writeUI8(self.bitmapCache)

        if self.visible is not None:
            if self.visible > 1:
                raise ValueError("bad value for visible")

            stream.writeUI8(self.visible)

        if self.backgroundColor is not None:
            stream.writeRGBA(self.backgroundColor)

        if self.clipActions is not None:
            if stream.version < 5:
                raise Exception("bad swf version")

            ClipActionRecord.writeArray(stream, self.clipActions)