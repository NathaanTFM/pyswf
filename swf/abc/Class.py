from __future__ import annotations
from swf.abc.Method import Method
from swf.abc.multinames.Multiname import Multiname
from swf.abc.namespaces.BaseNamespace import BaseNamespace
from swf.abc.multinames.QName import QName
from swf.abc.traits.Trait import Trait


class Class:
    name: QName
    superName: QName | None
    interfaces: list[Multiname]

    sealed: bool 
    final: bool
    interface: bool

    cinit: Method
    ctraits: list[Trait]
    
    iinit: Method
    itraits: list[Trait]
    
    protectedNs: BaseNamespace | None

    def __init__(self, name: QName):
        self.name = name
        self.superName = None
        self.interfaces = []

        self.sealed = False
        self.final = False
        self.interface = False

        self.ctraits = []
        self.itraits = []

        self.protectedNs = None


    def __repr__(self) -> str:
        return "Class(%r)" % self.name