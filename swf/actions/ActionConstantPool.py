from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionConstantPool(ActionRecord):
    code = 0x88

    constantPool: list[str]

    def __init__(self, constantPool: list[str]) -> None:
        self.constantPool = constantPool

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        count = stream.readUI16()
        constantPool = []

        for _ in range(count):
            constantPool.append(stream.readString())

        return ActionConstantPool(constantPool)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeUI16(len(self.constantPool))
        for string in self.constantPool:
            stream.writeString(string)