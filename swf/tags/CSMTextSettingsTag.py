from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class CSMTextSettingsTag(Tag):
    """
    The ShowFrame tag instructs Flash Player to display the
    contents of the display list. The file is paused for
    the duration of a single frame.
    """
    tagId = 74

    textId: int
    useFlashType: int
    gridFit: int
    thickness: float
    sharpness: float

    def __init__(self, textId: int, useFlashType: int, gridFit: int, thickness: float, sharpness: float) -> None:
        self.textId = textId
        self.useFlashType = useFlashType
        self.gridFit = gridFit
        self.thickness = thickness
        self.sharpness = sharpness


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 8:
            raise ValueError("bad swf version")
        
        textId = stream.readUI16()
        useFlashType = stream.readUB(2)
        gridFit = stream.readUB(3)
        if stream.readUB(3) != 0:
            raise Exception("reserved is non-zero")
        
        thickness = stream.readFLOAT()
        sharpness = stream.readFLOAT()
        
        if stream.readUI8() != 0:
            raise Exception("reserved is non-zero")
        
        return CSMTextSettingsTag(textId, useFlashType, gridFit, thickness, sharpness)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 8:
            raise ValueError("bad swf version")
        
        stream.writeUI16(self.textId)
        stream.writeUB(2, self.useFlashType)
        stream.writeUB(3, self.gridFit)
        stream.writeUB(3, 0)
        stream.writeFLOAT(self.thickness)
        stream.writeFLOAT(self.sharpness)
        stream.writeUI8(0)