from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class FileAttributesTag(Tag):
    """
    The FileAttributes tag definse characteristics of the
    SWF file. This tag is required for SWF 8 and later and
    must be the first tag in the SWF file.
    Additionally, the FileAttributes tag can optionally be
    included in all SWF versions.
    """
    tagId = 69

    useDirectBlit: bool
    useGPU: bool 
    hasMetadata: bool
    actionScript3: bool
    useNetwork: bool

    def __init__(self, useDirectBlit: bool, useGPU: bool, hasMetadata: bool, actionScript3: bool, useNetwork: bool) -> None:
        self.useDirectBlit = useDirectBlit
        self.useGPU = useGPU
        self.hasMetadata = hasMetadata
        self.actionScript3 = actionScript3
        self.useNetwork = useNetwork


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 8:
            raise ValueError("bad swf version")

        if stream.readUB(1) != 0:
            raise Exception("reserved is non zero")

        useDirectBlit = stream.readUB1()
        if useDirectBlit and stream.version < 10:
            raise Exception("bad swf version")

        useGPU = stream.readUB1()
        if useGPU and stream.version < 10:
            raise Exception("bad swf version")

        hasMetadata = stream.readUB1()
        actionScript3 = stream.readUB1()

        if stream.readUB(2) != 0:
            raise Exception("reserved is non zero")

        useNetwork = stream.readUB1()
        if stream.readUB(24) != 0:
            raise Exception("reserved is non zero")

        return FileAttributesTag(useDirectBlit, useGPU, hasMetadata, actionScript3, useNetwork)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 8:
            raise ValueError("bad swf version")

        # verify version
        if stream.version < 10 and (self.useDirectBlit or self.useGPU):
            raise Exception("bad swf version")

        stream.writeUB(1, 0)
        stream.writeUB1(self.useDirectBlit)
        stream.writeUB1(self.useGPU)
        stream.writeUB1(self.hasMetadata)
        stream.writeUB1(self.actionScript3)
        stream.writeUB(2, 0)
        stream.writeUB1(self.useNetwork)
        stream.writeUB(24, 0)