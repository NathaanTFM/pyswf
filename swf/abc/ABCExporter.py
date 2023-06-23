from __future__ import annotations
from swf.abc.ABCBytecode import ABCBytecode, ABCInstruction, ABCTarget
from swf.abc.ABCOutputStream import ABCOutputStream
from swf.abc.Instructions import Argument, Instructions
from swf.abc.Metadata import Metadata, MetadataItem
from swf.abc.Method import Method, MethodFlags, Param
from swf.abc.MethodBody import ABCException, MethodBody
from swf.abc.Script import Script
from swf.abc.Class import Class
from swf.abc.ABCInputStream import ABCInputStream
from swf.abc.constants.Null import Null
from swf.abc.constants.Undefined import Undefined
from swf.abc.namespaces.NamespaceDict import *
from swf.abc.multinames.MultinameDict import *
from swf.abc.traits.TraitDict import *

from swf.abc.ConstantPool import ConstantPool
from swf.abc.UniquePool import UniquePool

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import TypeVar, Callable
    from swf.abc.ValueType import ValueType
    from swf.abc.ABCFile import ABCFile

    T = TypeVar("T")

class ABCExporter:
    __abc: ABCFile

    # pools
    __integerPool: ConstantPool[int]
    __uintegerPool: ConstantPool[int]
    __doublePool: ConstantPool[float]
    __stringPool: ConstantPool[str]
    __namespacePool: ConstantPool[BaseNamespace]
    __nsSetPool: ConstantPool[tuple[BaseNamespace, ...]]
    __multinamePool: ConstantPool[BaseMultiname]
    __classes: UniquePool[Class]
    __methods: UniquePool[Method]

    # streams for constant pools
    __integerStream: ABCOutputStream
    __uintegerStream: ABCOutputStream
    __doubleStream: ABCOutputStream
    __stringStream: ABCOutputStream
    __namespaceStream: ABCOutputStream
    __nsSetStream: ABCOutputStream
    __multinameStream: ABCOutputStream

    # streams for unique pools and scripts
    __methodStream: ABCOutputStream
    __metadataStream: ABCOutputStream
    __instanceStream: ABCOutputStream
    __classStream: ABCOutputStream
    __scriptStream: ABCOutputStream
    __methodBodyStream: ABCOutputStream

    def __init__(self, abc: ABCFile):
        self.__abc = abc
        
        self.__integerPool = ConstantPool()
        self.__uintegerPool = ConstantPool()
        self.__doublePool = ConstantPool()
        self.__stringPool = ConstantPool()
        self.__namespacePool = ConstantPool()
        self.__nsSetPool = ConstantPool()
        self.__multinamePool = ConstantPool()
        self.__classes = UniquePool()
        self.__methods = UniquePool()


    def __clearPools(self) -> None:
        self.__integerPool.clear()
        self.__uintegerPool.clear()
        self.__doublePool.clear()
        self.__stringPool.clear()
        self.__namespacePool.clear()
        self.__nsSetPool.clear()
        self.__multinamePool.clear()
        self.__classes.clear()
        self.__methods.clear()


    def __clearStreams(self) -> None:
        self.__integerStream = ABCOutputStream()
        self.__uintegerStream = ABCOutputStream()
        self.__doubleStream = ABCOutputStream()
        self.__stringStream = ABCOutputStream()
        self.__namespaceStream = ABCOutputStream()
        self.__nsSetStream = ABCOutputStream()
        self.__multinameStream = ABCOutputStream()

        self.__methodStream = ABCOutputStream()
        self.__metadataStream = ABCOutputStream()
        self.__instanceStream = ABCOutputStream()
        self.__classStream = ABCOutputStream()
        self.__scriptStream = ABCOutputStream()
        self.__methodBodyStream = ABCOutputStream()


    def export(self) -> bytes:
        self.__clearPools()
        self.__clearStreams()

        for script in self.__abc.scripts:
            self.__writeScript(self.__scriptStream, script)
            
        for metadata in self.__abc.metadata:
            self.__writeMetadata(self.__metadataStream, metadata)

        stream = ABCOutputStream()
        stream.writeU16(self.__abc.minorVersion)
        stream.writeU16(self.__abc.majorVersion)
        
        # constant pools
        stream.writeU30(len(self.__integerPool)+1)
        stream.write(self.__integerStream.getBytes())
        
        stream.writeU30(len(self.__uintegerPool)+1)
        stream.write(self.__uintegerStream.getBytes())
        
        stream.writeU30(len(self.__doublePool)+1)
        stream.write(self.__doubleStream.getBytes())
        
        stream.writeU30(len(self.__stringPool)+1)
        stream.write(self.__stringStream.getBytes())
        
        stream.writeU30(len(self.__namespacePool)+1)
        stream.write(self.__namespaceStream.getBytes())
        
        stream.writeU30(len(self.__nsSetPool)+1)
        stream.write(self.__nsSetStream.getBytes())
        
        stream.writeU30(len(self.__multinamePool)+1)
        stream.write(self.__multinameStream.getBytes())

        stream.writeU30(len(self.__methods))
        stream.write(self.__methodStream.getBytes())
        
        stream.writeU30(len(self.__abc.metadata))
        stream.write(self.__metadataStream.getBytes())
        
        stream.writeU30(len(self.__classes))
        stream.write(self.__instanceStream.getBytes())
        stream.write(self.__classStream.getBytes())

        stream.writeU30(len(self.__abc.scripts))
        stream.write(self.__scriptStream.getBytes())

        bodyCount = 0
        for meth in self.__methods:
            if meth.body is not None:
                bodyCount += 1

        stream.writeU30(bodyCount)
        stream.write(self.__methodBodyStream.getBytes())

        return stream.getBytes()
    

    def __getConstantIndex(self, value: T | None, pool: ConstantPool[T], meth: Callable[[ABCOutputStream, T], None], stream: ABCOutputStream) -> int:
        if value is None:
            return 0
        
        index = pool.getIndex(value)
        if index is None:
            tempStream = ABCOutputStream()
            meth(tempStream, value)
            index = pool.append(value)
            stream.write(tempStream.getBytes())

        return index + 1
    

    def getIntegerIndex(self, value: int | None) -> int:
        return self.__getConstantIndex(value, self.__integerPool, self.__writeInteger, self.__integerStream)
    

    def getUIntegerIndex(self, value: int | None) -> int:
        return self.__getConstantIndex(value, self.__uintegerPool, self.__writeUInteger, self.__uintegerStream)
    

    def getDoubleIndex(self, value: float | None) -> int:
        return self.__getConstantIndex(value, self.__doublePool, self.__writeDouble, self.__doubleStream)
    

    def getStringIndex(self, value: str | None) -> int:
        return self.__getConstantIndex(value, self.__stringPool, self.__writeString, self.__stringStream)
    

    def getNamespaceIndex(self, value: BaseNamespace | None) -> int:
        return self.__getConstantIndex(value, self.__namespacePool, self.__writeNamespace, self.__namespaceStream)
    

    def getNsSetIndex(self, value: tuple[BaseNamespace, ...] | None) -> int:
        return self.__getConstantIndex(value, self.__nsSetPool, self.__writeNsSet, self.__nsSetStream)
    

    def getMultinameIndex(self, value: BaseMultiname | None) -> int:
        return self.__getConstantIndex(value, self.__multinamePool, self.__writeMultiname, self.__multinameStream)
    

    def getClassIndex(self, cls: Class) -> int:
        index = self.__classes.getIndex(cls)
        if index is None:
            # write instance
            instanceStream = ABCOutputStream()
            self.__writeInstance(instanceStream, cls)

            # write class
            classStream = ABCOutputStream()
            self.__writeClass(classStream, cls)

            index = self.__classes.append(cls)

            # write to main stream
            self.__instanceStream.write(instanceStream.getBytes())
            self.__classStream.write(classStream.getBytes())

        return index
    

    def getMethodIndex(self, method: Method) -> int:
        index = self.__methods.getIndex(method)
        if index is None:
            stream = ABCOutputStream()
            self.__writeMethod(stream, method)
            index = self.__methods.append(method)
            self.__methodStream.write(stream.getBytes())

            if method.body is not None:
                stream = ABCOutputStream()
                self.__writeMethodBody(stream, index, method.body)
                self.__methodBodyStream.write(stream.getBytes())

        return index
    

    def __writeInteger(self, stream: ABCOutputStream, value: int) -> None:
        stream.writeS32(value)


    def __writeUInteger(self, stream: ABCOutputStream, value: int) -> None:
        stream.writeS32(value)


    def __writeDouble(self, stream: ABCOutputStream, value: float) -> None:
        stream.writeD64(value)


    def __writeString(self, stream: ABCOutputStream, value: str) -> None:
        utf8 = value.encode("utf8")
        stream.writeU30(len(utf8))
        stream.write(utf8)


    def __writeNamespace(self, stream: ABCOutputStream, value: BaseNamespace) -> None:
        stream.writeU8(value.kind)
        stream.writeU30(self.getStringIndex(value.name))


    def __writeNsSet(self, stream: ABCOutputStream, value: tuple[BaseNamespace, ...]) -> None:
        stream.writeU30(len(value))
        for namespace in value:
            stream.writeU30(self.getNamespaceIndex(namespace))


    def __writeMultiname(self, stream: ABCOutputStream, value: BaseMultiname) -> None:
        stream.writeU8(value.kind)
        if isinstance(value, QName):
            stream.writeU30(self.getNamespaceIndex(value.ns))
            stream.writeU30(self.getStringIndex(value.name))

        elif isinstance(value, RTQName):
            stream.writeU30(self.getStringIndex(value.name))

        elif isinstance(value, RTQNameL):
            pass

        elif isinstance(value, Multiname):
            stream.writeU30(self.getStringIndex(value.name))
            stream.writeU30(self.getNsSetIndex(value.nsSet))

        elif isinstance(value, MultinameL):
            stream.writeU30(self.getNsSetIndex(value.nsSet))

        elif isinstance(value, TypeName):
            assert len(value.params) == 1
            stream.writeU30(self.getMultinameIndex(value.qname))
            stream.writeU30(len(value.params))
            stream.writeU30(self.getMultinameIndex(value.params[0]))

        else:
            raise NotImplementedError(value)
        

    def __writeMethod(self, stream: ABCOutputStream, method: Method) -> None:
        stream.writeU30(len(method.params))
        stream.writeU30(self.getMultinameIndex(method.returnType))
        for param in method.params:
            stream.writeU30(self.getMultinameIndex(param.type))

        stream.writeU30(self.getStringIndex(method.name))

        # calc flags
        flags = MethodFlags(0)
        options = 0
        for param in method.params:
            if param.default is not None:
                flags |= MethodFlags.HAS_OPTIONAL
                options += 1

            elif flags & MethodFlags.HAS_OPTIONAL:
                raise Exception("missing optional parameter")

        if method.params and all(param.name is not None for param in method.params):
            flags |= MethodFlags.HAS_PARAM_NAMES

        if method.body:
            for instr in method.body.bytecode.code:
                if isinstance(instr, ABCInstruction):
                    if instr.name == "newactivation":
                        flags |= MethodFlags.NEED_ACTIVATION

                    elif instr.name in ("dxns", "dxnslate"):
                        flags |= MethodFlags.SET_DXNS
        else:
            # we don't have a body, so grab those flags from the method
            flags |= method.flags & MethodFlags.NEED_ACTIVATION
            flags |= method.flags & MethodFlags.SET_DXNS

        # we take those two from method flags cause we can't guess that
        flags |= method.flags & MethodFlags.NEED_ARGUMENTS
        flags |= method.flags & MethodFlags.NEED_REST
                
        stream.writeU8(flags.value)

        if flags & MethodFlags.HAS_OPTIONAL:
            stream.writeU30(options)
            for param in method.params[len(method.params) - options:]:
                assert param.default is not None
                kind, val = self.__getKindVal(param.type, param.default)
                stream.writeU30(val)
                stream.writeU8(kind)

        if flags & MethodFlags.HAS_PARAM_NAMES:
            for param in method.params:
                stream.writeU30(self.getStringIndex(param.name))

        
    def __writeMetadata(self, stream: ABCOutputStream, metadata: Metadata) -> None:
        stream.writeU30(self.getStringIndex(metadata.name))
        stream.writeU30(len(metadata.items))
        for item in metadata.items:
            stream.writeU30(self.getStringIndex(item.key))
            stream.writeU30(self.getStringIndex(item.value))
        

    def __writeInstance(self, stream: ABCOutputStream, cls: Class) -> None:
        stream.writeU30(self.getMultinameIndex(cls.name))
        stream.writeU30(self.getMultinameIndex(cls.superName))
        
        flags = 0
        if cls.sealed: flags |= 0x01
        if cls.final: flags |= 0x02
        if cls.interface: flags |= 0x04
        if cls.protectedNs is not None: flags |= 0x08

        stream.writeU8(flags)
        
        if cls.protectedNs is not None:
            stream.writeU30(self.getNamespaceIndex(cls.protectedNs))

        stream.writeU30(len(cls.interfaces))
        for interface in cls.interfaces:
            stream.writeU30(self.getMultinameIndex(interface))

        stream.writeU30(self.getMethodIndex(cls.iinit))
        
        stream.writeU30(len(cls.itraits))
        for trait in cls.itraits:
            self.__writeTrait(stream, trait)

    
    def __writeClass(self, stream: ABCOutputStream, cls: Class) -> None:
        stream.writeU30(self.getMethodIndex(cls.cinit))
        
        stream.writeU30(len(cls.ctraits))
        for trait in cls.ctraits:
            self.__writeTrait(stream, trait)


    def __writeScript(self, stream: ABCOutputStream, script: Script) -> None:
        stream.writeU30(self.getMethodIndex(script.init))
        
        stream.writeU30(len(script.traits))
        for trait in script.traits:
            self.__writeTrait(stream, trait)


    def __writeMethodBody(self, stream: ABCOutputStream, index: int, body: MethodBody) -> None:
        stream.writeU30(index)
        stream.writeU30(body.maxStack)
        stream.writeU30(body.localCount)
        stream.writeU30(body.initScopeDepth)
        stream.writeU30(body.maxScopeDepth)

        code = body.bytecode.assemble(self)
        stream.writeU30(len(code))
        stream.write(code)

        stream.writeU30(len(body.exceptions))
        for exc in body.exceptions:
            assert body.bytecode.targets is not None
            stream.writeU30(body.bytecode.targets[exc.from_.id])
            stream.writeU30(body.bytecode.targets[exc.to.id])
            stream.writeU30(body.bytecode.targets[exc.target.id])
            stream.writeU30(self.getMultinameIndex(exc.excType))
            stream.writeU30(self.getMultinameIndex(exc.varName))

        stream.writeU30(len(body.traits))
        for trait in body.traits:
            self.__writeTrait(stream, trait)


    def __writeTrait(self, stream: ABCOutputStream, trait: Trait) -> None:
        stream.writeU30(self.getMultinameIndex(trait.name))

        attr = 0
        if isinstance(trait, TraitMethod):
            if trait.final:
                attr |= 0x01
            if trait.override:
                attr |= 0x02

        if trait.metadata is not None:
            attr |= 0x04

        stream.writeU8(trait.kind | (attr << 4))

        if isinstance(trait, TraitSlot):
            stream.writeU30(trait.slotId)
            stream.writeU30(self.getMultinameIndex(trait.type))
            
            kind, value = self.__getKindVal(trait.type, trait.value)
            stream.writeU30(value)
            if value:
                stream.writeU8(kind)

        elif isinstance(trait, TraitClass):
            stream.writeU30(trait.slotId)
            stream.writeU30(self.getClassIndex(trait.classi))

        elif isinstance(trait, TraitMethod):
            stream.writeU30(trait.dispId)
            stream.writeU30(self.getMethodIndex(trait.method))

        if trait.metadata is not None:
            stream.writeU30(len(trait.metadata))
            for metadata in trait.metadata:
                stream.writeU30(self.__abc.metadata.index(metadata))


    def __getKindVal(self, vtype: BaseMultiname | None, value: ValueType) -> tuple[int, int]:
        assert value is not None

        if value is True:
            return 0x0B, 0x0B

        elif value is False:
            return 0x0A, 0x0A 

        elif value == Null:
            return 0x0C, 0x0C

        elif value == Undefined:
            return 0x00, 0x00

        elif type(value) == int:
            if False and isinstance(vtype, QName) and vtype.name == "uint":
                return 0x04, self.getUIntegerIndex(value)
            else:
                return 0x03, self.getIntegerIndex(value)

        elif type(value) == float:
            return 0x06, self.getDoubleIndex(value)

        elif type(value) == str:
            return 0x01, self.getStringIndex(value)

        elif isinstance(value, BaseNamespace):
            return value.kind, self.getNamespaceIndex(value)

        else:
            raise Exception("not supported value %r" % value)

