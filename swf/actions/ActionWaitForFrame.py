from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionWaitForFrame(ActionRecord):
    code = 0x8A

    frame: int
    skipCount: int

    def __init__(self, frame: int, skipCount: int) -> None:
        self.frame = frame
        self.skipCount = skipCount

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        frame = stream.readUI16()
        skipCount = stream.readUI8()
        return ActionWaitForFrame(frame, skipCount)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeUI16(self.frame)
        stream.writeUI8(self.skipCount)