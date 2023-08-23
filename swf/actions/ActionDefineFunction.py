from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

from swf.stream import ActionStream

class ActionDefineFunction(ActionRecord):
    code = 0x9B

    functionName: str
    params: list[str]
    codeSize: int

    def __init__(self, functionName: str, params: list[str], codeSize: int) -> None:
        self.functionName = functionName
        self.params = params
        self.codeSize = codeSize # TODO: make it better

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        functionName = stream.readString()
        numParams = stream.readUI16()
        params = []
        for _ in range(numParams):
            params.append(stream.readString())

        codeSize = stream.readUI16()
        return ActionDefineFunction(functionName, params, codeSize)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeString(self.functionName)
        stream.writeUI16(len(self.params))
        for param in self.params:
            stream.writeString(param)

        stream.writeUI16(self.codeSize)