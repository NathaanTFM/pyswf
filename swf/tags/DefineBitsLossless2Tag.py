from __future__ import annotations
from swf.records.RGBA import RGBA
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
import zlib

class DefineBitsLossless2Tag(Tag):
    """
    DefineBitsLossless2 extends DefineBitsLossless with support
    for opacity (alpha values).
    """
    tagId = 36

    characterId: int
    bitmapFormat: int
    bitmapWidth: int
    bitmapHeight: int
    pixelData: list[RGBA]

    def __init__(self, characterId: int, bitmapFormat: int, bitmapWidth: int, bitmapHeight: int, pixelData: list[RGBA]) -> None:
        self.characterId = characterId
        self.bitmapFormat = bitmapFormat
        self.bitmapWidth = bitmapWidth
        self.bitmapHeight = bitmapHeight
        self.pixelData = pixelData
        

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")

        characterId = stream.readUI16()
        bitmapFormat = stream.readUI8()
        if bitmapFormat not in (3, 5):
            raise ValueError("bad bitmap format")

        bitmapWidth = stream.readUI16()
        bitmapHeight = stream.readUI16()
        
        if bitmapFormat == 3:
            bitmapColorTableSize = stream.readUI8()
        
        zlibBitmapData = stream.read(stream.available())
        bitmapData = SWFInputStream(stream.version, zlib.decompress(zlibBitmapData))
        
        if bitmapFormat == 3:
            # AlphaColorMapData
            padding = (4 - bitmapWidth % 4) % 4

            colorTableRGBA = [bitmapData.readRGBA() for n in range(bitmapColorTableSize + 1)]
            colormapPixelData = []
            
            for height in range(bitmapHeight):
                for width in range(bitmapWidth):
                    colormapPixelData.append(bitmapData.readUI8())
                
                if padding:
                    bitmapData.skip(padding)
            
            pixelData = [colorTableRGBA[x] for x in colormapPixelData]
            
        else:
            # BitmapData
            bitmapPixelData: list[RGBA] = []
            for height in range(bitmapHeight):
                for width in range(bitmapWidth):
                    bitmapPixelData.append(bitmapData.readARGB())
                    
            pixelData = bitmapPixelData

        assert bitmapData.available() == 0
        return DefineBitsLossless2Tag(characterId, bitmapFormat, bitmapWidth, bitmapHeight, pixelData)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        if self.bitmapFormat not in (3, 5):
            raise ValueError("bad bitmap format")

        stream.writeUI16(self.characterId)
        stream.writeUI8(self.bitmapFormat)
        stream.writeUI16(self.bitmapWidth)
        stream.writeUI16(self.bitmapHeight)

        bitmapData = SWFOutputStream(stream.version)

        if self.bitmapFormat == 3:
            padding = (4 - self.bitmapWidth % 4) % 4
            colorTableRGBA: list[RGBA] = []

            for color in self.pixelData:
                if color not in colorTableRGBA:
                    colorTableRGBA.append(color)
                    bitmapData.writeRGBA(color)

            for y in range(self.bitmapHeight):
                for x in range(self.bitmapWidth):
                    color = self.pixelData[x + y * self.bitmapWidth]
                    bitmapData.writeUI8(colorTableRGBA.index(color))

                bitmapData.write(b"\0" * padding)

            stream.writeUI8(len(colorTableRGBA) - 1)

        else:
            for y in range(self.bitmapHeight):
                for x in range(self.bitmapWidth):
                    color = self.pixelData[x + y * self.bitmapWidth]
                    bitmapData.writeARGB(color)


        stream.write(zlib.compress(bitmapData.getBytes(), 9))