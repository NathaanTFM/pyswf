from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionSetTarget(ActionRecord):
    code = 0x8B

    targetName: str

    def __init__(self, targetName: str) -> None:
        self.targetName = targetName

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        targetName = stream.readString()
        return ActionSetTarget(targetName)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeString(self.targetName)