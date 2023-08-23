from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionStoreRegister(ActionRecord):
    code = 0x87

    registerNumber: int

    def __init__(self, registerNumber: int) -> None:
        self.registerNumber = registerNumber

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        registerNumber = stream.readUI8()
        return ActionStoreRegister(registerNumber)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeUI8(self.registerNumber)