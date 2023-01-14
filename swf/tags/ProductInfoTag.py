from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class ProductInfoTag(Tag):
    """
    Non-documented SWF tag
    """
    tagId = 41

    productId: int
    edition: int
    majorVersion: int
    minorVersion: int
    buildNumber: int
    compilationDate: int

    def __init__(self, productId: int, edition: int, majorVersion: int, minorVersion: int, buildNumber: int, compilationDate: int) -> None:
        self.productId = productId
        self.edition = edition
        self.majorVersion = majorVersion
        self.minorVersion = minorVersion
        self.buildNumber = buildNumber
        self.compilationDate = compilationDate


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")
    
        productId = stream.readUI32()
        edition = stream.readUI32()
        majorVersion = stream.readUI8()
        minorVersion = stream.readUI8()
        buildNumber = stream.readUI64()
        compilationDate = stream.readUI64()
        return ProductInfoTag(productId, edition, majorVersion, minorVersion, buildNumber, compilationDate)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")

        stream.writeUI32(self.productId)
        stream.writeUI32(self.edition)
        stream.writeUI8(self.majorVersion)
        stream.writeUI8(self.minorVersion)
        stream.writeUI64(self.buildNumber)
        stream.writeUI64(self.compilationDate)