from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.abc.Method import Method
    
from swf.abc import ABCBytecode
from swf.abc.multinames.BaseMultiname import BaseMultiname
from swf.abc.traits.Trait import Trait

class ABCException:
    from_: ABCBytecode.ABCTarget
    to: ABCBytecode.ABCTarget
    target: ABCBytecode.ABCTarget
    excType: BaseMultiname | None
    varName: BaseMultiname | None
    
    def __init__(self, from_: ABCBytecode.ABCTarget, to: ABCBytecode.ABCTarget, target: ABCBytecode.ABCTarget, excType: BaseMultiname | None, varName: BaseMultiname | None):
        self.from_ = from_
        self.to = to
        self.target = target
        self.excType = excType
        self.varName = varName


class MethodBody:   
    maxStack: int
    localCount: int
    initScopeDepth: int
    maxScopeDepth: int
    bytecode: ABCBytecode.ABCBytecode
    exceptions: list[ABCException]
    traits: list[Trait]

    def __init__(self, maxStack: int, localCount: int, initScopeDepth: int, maxScopeDepth: int, bytecode: ABCBytecode.ABCBytecode | None = None):
        self.maxStack = maxStack
        self.localCount = localCount
        self.initScopeDepth = initScopeDepth
        self.maxScopeDepth = maxScopeDepth
        self.bytecode = bytecode if bytecode is not None else ABCBytecode.ABCBytecode()
        self.exceptions = []
        self.traits = []