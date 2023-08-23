from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionGotoFrame(ActionRecord):
    code = 0x81

    def __init__(self, frame: int) -> None:
        self.frame = frame

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        frame = stream.readUI16()
        return ActionGotoFrame(frame)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeUI16(self.frame)