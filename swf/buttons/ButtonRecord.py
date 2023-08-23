from __future__ import annotations
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.records.Matrix import Matrix
from swf.records.ColorTransformWithAlpha import ColorTransformWithAlpha
from swf.filters.Filter import Filter
from swf.filters.FilterList import FilterList

class ButtonRecord:
    stateHitTest: bool
    stateDown: bool
    stateOver: bool
    stateUp: bool

    characterId: int
    placeDepth: int
    placeMatrix: Matrix

    # DefineButton2
    colorTransform: ColorTransformWithAlpha | None
    filterList: list[Filter] | None
    blendMode: int | None

    def __init__(self, stateHitTest: bool, stateDown: bool, stateOver: bool, stateUp: bool, characterId: int, placeDepth: int, placeMatrix: Matrix, colorTransform: ColorTransformWithAlpha | None, filterList: list[Filter] | None, blendMode: int | None):
        self.stateHitTest = stateHitTest
        self.stateDown = stateDown
        self.stateOver = stateOver
        self.stateUp = stateUp

        self.characterId = characterId
        self.placeDepth = placeDepth
        self.placeMatrix = placeMatrix

        self.colorTransform = colorTransform
        self.filterList = filterList
        self.blendMode = blendMode


    @staticmethod
    def read(stream: SWFInputStream, tag: int) -> ButtonRecord | None:
        if stream.readUB(2) != 0:
            raise Exception("reserved is non-zero")
        
        hasBlendMode = stream.readUB1()
        hasFilterList = stream.readUB1()
        if tag != 2 and (hasBlendMode or hasFilterList):
            raise Exception("has blend mode or filter list in wrong tag")
        
        stateHitTest = stream.readUB1()
        stateDown = stream.readUB1()
        stateOver = stream.readUB1()
        stateUp = stream.readUB1()

        # we've read a byte, if nothing was set then there's no buttonrecord
        if not (stateHitTest or stateDown or stateOver or stateUp or hasBlendMode or hasFilterList):
            return None

        characterId = stream.readUI16()
        placeDepth = stream.readUI16()
        placeMatrix = stream.readMATRIX()

        colorTransform = filterList = blendMode = None
        if tag == 2:
            colorTransform = stream.readCXFORMWITHALPHA()

            if hasFilterList:
                filterList = []

                numberOfFilters = stream.readUI8()
                for _ in range(numberOfFilters):
                    filterId = stream.readUI8()
                    filter = FilterList[filterId].read(stream)
                    filterList.append(filter)

            if hasBlendMode:
                blendMode = stream.readUI8()

        return ButtonRecord(stateHitTest, stateDown, stateOver, stateUp, characterId, placeDepth, placeMatrix, colorTransform, filterList, blendMode)
    

    def write(self, stream: SWFOutputStream, tag: int) -> None:
        stream.writeUB(2, 0)

        if tag != 2 and (self.blendMode is not None or self.filterList is not None):
            raise Exception("has blend mode or filter list in wrong tag")
        
        stream.writeUB1(self.blendMode is not None)
        stream.writeUB1(self.filterList is not None)
        stream.writeUB1(self.stateHitTest)
        stream.writeUB1(self.stateDown)
        stream.writeUB1(self.stateOver)
        stream.writeUB1(self.stateUp)

        # sanity check
        if not (self.stateHitTest or self.stateDown or self.stateOver or self.stateUp or self.blendMode is not None or self.filterList is not None):
            raise Exception("buttonrecord does not exist")

        stream.writeUI16(self.characterId)
        stream.writeUI16(self.placeDepth)
        stream.writeMATRIX(self.placeMatrix)

        if tag == 2:
            if self.colorTransform is None:
                raise Exception("color transform is none but tag is 2")
            
            stream.writeCXFORMWITHALPHA(self.colorTransform)

            if self.filterList is not None:
                stream.writeUI8(len(self.filterList))
                for filter in self.filterList:
                    stream.writeUI8(filter.id)
                    filter.write(stream)

            if self.blendMode is not None:
                stream.writeUI8(self.blendMode)