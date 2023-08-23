from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionTry(ActionRecord):
    code = 0x8F

    finallyBlock: bool
    catchBlock: bool

    trySize: int
    catchSize: int
    finallySize: int

    catchName: str | None
    catchRegister: int | None

    def __init__(self, finallyBlock: bool, catchBlock: bool, trySize: int, catchSize: int, finallySize: int, catchName: str | None, catchRegister: int | None) -> None:
        self.finallyBlock = finallyBlock
        self.catchBlock = catchBlock
        self.trySize = trySize
        self.catchSize = catchSize
        self.finallySize = finallySize
        self.catchName = catchName
        self.catchRegister = catchRegister

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        if stream.readUB(5) != 0:
            raise Exception("reserved is non-zero")
        
        catchInRegister = stream.readUB1()
        finallyBlock = stream.readUB1()
        catchBlock = stream.readUB1()

        trySize = stream.readUI16()
        catchSize = stream.readUI16()
        finallySize = stream.readUI16()

        catchName = catchRegister = None
        if catchInRegister:
            catchRegister = stream.readUI8()
        else:
            catchName = stream.readString()

        return ActionTry(finallyBlock, catchBlock, trySize, catchSize, finallySize, catchName, catchRegister)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        if (self.catchRegister is None) == (self.catchName is None):
            raise Exception("only one of catchRegister/catchName must be set")

        stream.writeUB(5, 0)
        stream.writeUB1(self.catchRegister is not None)
        stream.writeUB1(self.finallyBlock)
        stream.writeUB1(self.catchBlock)

        stream.writeUI16(self.trySize)
        stream.writeUI16(self.catchSize)
        stream.writeUI16(self.finallySize)

        if self.catchRegister is not None:
            stream.writeUI8(self.catchRegister)
        elif self.catchName is not None:
            stream.writeString(self.catchName)
