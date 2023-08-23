from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionGoToLabel(ActionRecord):
    code = 0x8C

    label: str

    def __init__(self, label: str) -> None:
        self.label = label

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        label = stream.readString()
        return ActionGoToLabel(label)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeString(self.label)