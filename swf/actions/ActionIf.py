from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionIf(ActionRecord):
    code = 0x9D

    branchOffset: int

    def __init__(self, branchOffset: int) -> None:
        self.branchOffset = branchOffset

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        branchOffset = stream.readSI16()
        return ActionIf(branchOffset)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeSI16(self.branchOffset)