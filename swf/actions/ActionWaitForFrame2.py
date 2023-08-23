from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionWaitForFrame2(ActionRecord):
    code = 0x8D

    skipCount: int

    def __init__(self, skipCount: int) -> None:
        self.skipCount = skipCount

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        skipCount = stream.readUI8()
        return ActionWaitForFrame2(skipCount)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeUI8(self.skipCount)