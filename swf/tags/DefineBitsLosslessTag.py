from __future__ import annotations
from swf.records.RGB import RGB
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from typing import overload
import zlib

class DefineBitsLosslessTag(Tag):
    """
    Defines a lossless bitmap character that contains
    RGB bitmap data compressed with ZLIB.
    """
    tagId = 20

    characterId: int
    bitmapFormat: int
    bitmapWidth: int
    bitmapHeight: int
    bitmapColorTableSize: int | None
    bitmapData: bytes | None

    def __init__(self, characterId: int, bitmapFormat: int, bitmapWidth: int, bitmapHeight: int, bitmapColorTableSize: int | None, bitmapData: bytes | None) -> None:
        self.characterId = characterId
        self.bitmapFormat = bitmapFormat
        self.bitmapWidth = bitmapWidth
        self.bitmapHeight = bitmapHeight
        self.bitmapColorTableSize = bitmapColorTableSize
        self.bitmapData = bitmapData


    def getPixelData(self) -> list[RGB]:
        if self.bitmapData is None:
            raise TypeError("bitmapData is None")
        
        bitmapData = SWFInputStream(0, self.bitmapData)
        
        if self.bitmapFormat == 3:
            if self.bitmapColorTableSize is None:
                raise TypeError("bitmapColorTableSize is None for bitmapFormat 3")
            
            # ColorMapData
            padding = (4 - self.bitmapWidth % 4) % 4

            colorTableRGB = [bitmapData.readRGB() for n in range(self.bitmapColorTableSize + 1)]
            colormapPixelData = []
            
            for y in range(self.bitmapHeight):
                for x in range(self.bitmapWidth):
                    colormapPixelData.append(bitmapData.readUI8())
                
                if padding:
                    bitmapData.skip(padding)
            
            pixelData = [colorTableRGB[x] for x in colormapPixelData]
            
        else:
            # BitmapData
            bitmapPixelData: list[RGB] = []
            for y in range(self.bitmapHeight):
                for x in range(self.bitmapWidth):
                    if self.bitmapFormat == 4: # 15 bit
                        bitmapData.readUB(1)
                        bitmapPixelData.append(RGB(bitmapData.readUB(5), bitmapData.readUB(5), bitmapData.readUB(5)))

                    elif self.bitmapFormat == 5: # 24 bit
                        bitmapData.skip(1)
                        bitmapPixelData.append(RGB(bitmapData.readUI8(), bitmapData.readUI8(), bitmapData.readUI8()))
                    
            pixelData = bitmapPixelData

        assert bitmapData.available() == 0
        return pixelData
    

    def setPixelData(self, pixelData: list[RGB]) -> None:
        bitmapData = SWFOutputStream(0)

        if self.bitmapFormat == 3:
            padding = (4 - self.bitmapWidth % 4) % 4
            colorTableRGB: list[RGB] = []

            for color in pixelData:
                if color not in colorTableRGB:
                    colorTableRGB.append(color)
                    bitmapData.writeRGB(color)

            for y in range(self.bitmapHeight):
                for x in range(self.bitmapWidth):
                    color = pixelData[x + y * self.bitmapWidth]
                    bitmapData.writeUI8(colorTableRGB.index(color))

                bitmapData.write(b"\0" * padding)

            self.bitmapColorTableSize = len(colorTableRGB) - 1

        else:
            self.bitmapColorTableSize = None

            for y in range(self.bitmapHeight):
                for x in range(self.bitmapWidth):
                    color = pixelData[x + y * self.bitmapWidth]
                    if self.bitmapFormat == 4: # 15 bit
                        bitmapData.writeUB(1, 0)
                        bitmapData.writeUB(5, color.red)
                        bitmapData.writeUB(5, color.green)
                        bitmapData.writeUB(5, color.blue)

                    elif self.bitmapFormat == 5: # 24 bit
                        bitmapData.writeUI8(0xFF) # flash writes 0xFF
                        bitmapData.writeUI8(color.red)
                        bitmapData.writeUI8(color.green)
                        bitmapData.writeUI8(color.blue)

        self.bitmapData = bitmapData.getBytes()


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 2:
            raise ValueError("bad swf version")

        characterId = stream.readUI16()
        bitmapFormat = stream.readUI8()
        if bitmapFormat not in (3, 4, 5):
            raise ValueError("bad bitmap format")

        bitmapWidth = stream.readUI16()
        bitmapHeight = stream.readUI16()
        
        bitmapColorTableSize = None
        if bitmapFormat == 3:
            bitmapColorTableSize = stream.readUI8()
        
        zlibBitmapData = stream.read(stream.available())
        bitmapData = zlib.decompress(zlibBitmapData)

        return DefineBitsLosslessTag(characterId, bitmapFormat, bitmapWidth, bitmapHeight, bitmapColorTableSize, bitmapData)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 2:
            raise ValueError("bad swf version")

        if self.bitmapFormat not in (3, 4, 5):
            raise ValueError("bad bitmap format")

        stream.writeUI16(self.characterId)
        stream.writeUI8(self.bitmapFormat)
        stream.writeUI16(self.bitmapWidth)
        stream.writeUI16(self.bitmapHeight)

        if self.bitmapFormat == 3:
            if self.bitmapColorTableSize is None:
                raise TypeError("bitmapColorTableSize is None for bitmapFormat 3")
            
            stream.writeUI8(self.bitmapColorTableSize)

        if self.bitmapData is None:
            raise TypeError("bitmapData is None")
        
        stream.write(zlib.compress(self.bitmapData, 9))