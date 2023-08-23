from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.records.ColorTransform import ColorTransform

class DefineButtonCxformTag(Tag):
    """
    DefineButtonCxform defines the color transform for each shape
    and text character in a button.
    """
    tagId = 23

    buttonId: int
    buttonColorTransform: ColorTransform
    
    def __init__(self, buttonId: int, buttonColorTransform: ColorTransform) -> None:
        self.buttonId = buttonId
        self.buttonColorTransform = buttonColorTransform


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 2:
            raise ValueError("bad swf version")
        
        buttonId = stream.readUI16()
        buttonColorTransform = stream.readCXFORM()
        return DefineButtonCxformTag(buttonId, buttonColorTransform)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 2:
            raise ValueError("bad swf version")
        
        stream.writeUI16(self.buttonId)
        stream.writeCXFORM(self.buttonColorTransform)