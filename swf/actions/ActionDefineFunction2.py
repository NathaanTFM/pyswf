from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionDefineFunction2(ActionRecord):
    code = 0x8E

    functionName: str
    registerCount: int

    preloadParent: bool
    preloadRoot: bool
    suppressSuper: bool
    preloadSuper: bool
    suppressArguments: bool
    preloadArguments: bool
    suppressThis: bool
    preloadThis: bool
    preloadGlobal: bool

    params: list[tuple[int, str]]
    codeSize: int

    def __init__(self, functionName: str, registerCount: int, preloadParent: bool, preloadRoot: bool, suppressSuper: bool, preloadSuper: bool, suppressArguments: bool, preloadArguments: bool, suppressThis: bool, preloadThis: bool, preloadGlobal: bool, params: list[tuple[int, str]], codeSize: int) -> None:
        self.functionName = functionName
        self.registerCount = registerCount

        self.preloadParent = preloadParent
        self.preloadRoot = preloadRoot
        self.suppressSuper = suppressSuper
        self.preloadSuper = preloadSuper
        self.suppressArguments = suppressArguments
        self.preloadArguments = preloadArguments
        self.suppressThis = suppressThis
        self.preloadThis = preloadThis
        self.preloadGlobal = preloadGlobal

        self.params = params
        self.codeSize = codeSize # TODO: make it better

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        functionName = stream.readString()
        numParams = stream.readUI16()

        registerCount = stream.readUI8()
        
        preloadParent = stream.readUB1()
        preloadRoot = stream.readUB1()
        suppressSuper = stream.readUB1()
        preloadSuper = stream.readUB1()
        suppressArguments = stream.readUB1()
        preloadArguments = stream.readUB1()
        suppressThis = stream.readUB1()
        preloadThis = stream.readUB1()

        if stream.readUB(7) != 0:
            raise Exception("reserved is non zero")
        
        preloadGlobal = stream.readUB1()

        params = []
        for _ in range(numParams):
            register = stream.readUI8()
            paramName = stream.readString()
            params.append((register, paramName))

        codeSize = stream.readUI16()
        return ActionDefineFunction2(functionName, registerCount, preloadParent, preloadRoot, suppressSuper, preloadSuper, suppressArguments, preloadArguments, suppressThis, preloadThis, preloadGlobal, params, codeSize)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeString(self.functionName)
        stream.writeUI16(len(self.params))

        stream.writeUI8(self.registerCount)

        stream.writeUB1(self.preloadParent)
        stream.writeUB1(self.preloadRoot)
        stream.writeUB1(self.suppressSuper)
        stream.writeUB1(self.preloadSuper)
        stream.writeUB1(self.suppressArguments)
        stream.writeUB1(self.preloadArguments)
        stream.writeUB1(self.suppressThis)
        stream.writeUB1(self.preloadThis)
        stream.writeUB(7, 0)
        stream.writeUB1(self.preloadGlobal)

        for register, paramName in self.params:
            stream.writeUI8(register)
            stream.writeString(paramName)
            
        stream.writeUI16(self.codeSize)