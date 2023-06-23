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
from swf.abc.ABCExporter import ABCExporter

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, TypeVar, Generator, TypeVar
    from swf.abc.ValueType import ValueType

    T = TypeVar("T")

class ABCFile:
    minorVersion: int
    majorVersion: int
    metadata: list[Metadata]
    scripts: list[Script]
    
    # constant pool
    __integerPool: ConstantPool[int]
    __uintegerPool: ConstantPool[int]
    __doublePool: ConstantPool[float]
    __stringPool: ConstantPool[str]
    __namespacePool: ConstantPool[BaseNamespace]
    __nsSetPool: ConstantPool[tuple[BaseNamespace, ...]]
    __multinamePool: ConstantPool[BaseMultiname]

    # also other pools
    __methods: UniquePool[Method]
    __classes: UniquePool[Class]

    def __init__(self, data: bytes | None = None) -> None:
        self.__integerPool = ConstantPool()
        self.__uintegerPool = ConstantPool()
        self.__doublePool = ConstantPool()
        self.__stringPool = ConstantPool()
        self.__namespacePool = ConstantPool()
        self.__nsSetPool = ConstantPool()
        self.__multinamePool = ConstantPool()
        self.__methods = UniquePool()
        self.__classes = UniquePool()

        if data:
            stream = ABCInputStream(data)
            self.minorVersion = stream.readU16()
            self.majorVersion = stream.readU16()
            
            self.__readConstantPool(stream)
            self.__readMethodInfo(stream)
            self.__readMetadataInfo(stream)
            self.__readClassInfo(stream)
            self.__readScriptInfo(stream)
            self.__readMethodBodyInfo(stream)
            
            if stream.available():
                raise Exception("Data left after reading everything")

        else:
            self.minorVersion = 16
            self.majorVersion = 46

            self.metadata = []
            self.scripts = []


    def __getConstant(self, index: int, pool: ConstantPool[T]) -> T | None:
        if index == 0:
            return None
        
        return pool.getItem(index-1)
    

    def getInteger(self, index: int) -> int | None:
        return self.__getConstant(index, self.__integerPool)
    

    def getUInteger(self, index: int) -> int | None:
        return self.__getConstant(index, self.__uintegerPool)
    

    def getDouble(self, index: int) -> float | None:
        return self.__getConstant(index, self.__doublePool)
    

    def getString(self, index: int) -> str | None:
        return self.__getConstant(index, self.__stringPool)
    

    def getNamespace(self, index: int) -> BaseNamespace | None:
        return self.__getConstant(index, self.__namespacePool)
    

    def getNsSet(self, index: int) -> tuple[BaseNamespace, ...] | None:
        return self.__getConstant(index, self.__nsSetPool)
    

    def getMultiname(self, index: int) -> BaseMultiname | None:
        return self.__getConstant(index, self.__multinamePool)
    

    def getClass(self, index: int) -> Class:
        return self.__classes.getItem(index)
    

    def getMethod(self, index: int) -> Method:
        return self.__methods.getItem(index)

            
    def getTraits(self, trait: Trait | None = None) -> Generator[Trait, None, None]:
        if trait is not None:
            yield trait
            if isinstance(trait, TraitClass):
                for trait2 in trait.classi.ctraits:
                    yield from self.getTraits(trait2)
                    
                for trait2 in trait.classi.itraits:
                    yield from self.getTraits(trait2)

            elif isinstance(trait, TraitFunction):
                if trait.function.body:
                    for trait2 in trait.function.body.traits:
                        yield from self.getTraits(trait2)

            elif isinstance(trait, TraitMethod):
                if trait.method.body:
                    for trait2 in trait.method.body.traits:
                        yield from self.getTraits(trait2)
                
        else:
            for script in self.scripts:
                for trait2 in script.traits:
                    yield from self.getTraits(trait2)
            

    def __readConstantPool(self, stream: ABCInputStream) -> None:
        self.__integerPool.clear()
        self.__uintegerPool.clear()
        self.__doublePool.clear()
        self.__stringPool.clear()
        self.__namespacePool.clear()
        self.__nsSetPool.clear()
        self.__multinamePool.clear()

        # read integer pool
        intCount = stream.readU30()
        for _ in range(1, intCount):
            self.__integerPool.append(stream.readS32())

        # read uinteger pool
        uintCount = stream.readU30()
        for _ in range(1, uintCount):
            self.__uintegerPool.append(stream.readU32())

        # read double pool
        doubleCount = stream.readU30()
        for _ in range(1, doubleCount):
            self.__doublePool.append(stream.readD64())

        # read string pool
        stringCount = stream.readU30()
        for _ in range(1, stringCount):
            self.__stringPool.append(stream.read(stream.readU30()).decode("utf8"))

        # read namespace pool
        namespaceCount = stream.readU30()
        for _ in range(1, namespaceCount):
            nsType = NamespaceDict[stream.readU8()]
            name = self.getString(stream.readU30())
            self.__namespacePool.append(nsType(name))

        # read nsset pool
        nsSetCount = stream.readU30()
        for _ in range(1, nsSetCount):
            count = stream.readU30()
            nsSetTmp: list[BaseNamespace] = []
            for _ in range(count):
                ns = self.getNamespace(stream.readU30())
                assert ns is not None

                nsSetTmp.append(ns)

            self.__nsSetPool.append(tuple(nsSetTmp))

        # read multiname pool
        multinameCount = stream.readU30()
        for _ in range(1, multinameCount):
            multinameType = MultinameDict[stream.readU8()]

            if issubclass(multinameType, QName):
                ns = self.getNamespace(stream.readU30())
                name = self.getString(stream.readU30())
                self.__multinamePool.append(multinameType(ns, name))

            elif issubclass(multinameType, RTQName):
                name = self.getString(stream.readU30())
                self.__multinamePool.append(multinameType(name))

            elif issubclass(multinameType, RTQNameL):
                self.__multinamePool.append(multinameType())

            elif issubclass(multinameType, Multiname):
                name = self.getString(stream.readU30())
                nsSet = self.getNsSet(stream.readU30())
                if nsSet is None:
                    raise Exception("nsSet cannot be None")

                self.__multinamePool.append(multinameType(name, nsSet))

            elif issubclass(multinameType, MultinameL):
                nsSet = self.getNsSet(stream.readU30())
                if nsSet is None:
                    raise Exception("nsSet cannot be None")

                self.__multinamePool.append(multinameType(nsSet))

            elif issubclass(multinameType, TypeName):
                qname = self.getMultiname(stream.readU30())
                if type(qname) != QName:
                    raise Exception("expected QName")

                # avmplus apparently only supports count of 1
                count = stream.readU30()
                if count != 1:
                    raise Exception("count must be 1 (got %d)" % count)

                param = self.getMultiname(stream.readU30())

                # TODO: this might be allowed actually
                if param is None:
                    raise Exception("param can't be None")
                    
                self.__multinamePool.append(multinameType(qname, [param]))

            else:
                raise Exception("Can't read %s" % type)
            
    
    def __readMethodInfo(self, stream: ABCInputStream) -> None:
        self.__methods.clear()

        methodCount = stream.readU30()
        for _ in range(methodCount):
            meth = Method()
            self.__methods.append(meth)

            paramCount = stream.readU30()
            returnType = self.getMultiname(stream.readU30())
            if returnType is not None and not isinstance(returnType, (QName, TypeName)):
                raise Exception("return type is not a QName or TypeName (%r)" % returnType)

            meth.returnType = returnType

            for _ in range(paramCount):
                paramType = self.getMultiname(stream.readU30())
                if paramType is not None and not isinstance(paramType, (QName, TypeName)):
                    raise Exception("param type is not a QName or TypeName")         

                param = Param(paramType)
                meth.params.append(param)

            meth.name = self.getString(stream.readU30())
            meth.flags = MethodFlags(stream.readU8())

            if meth.flags & MethodFlags.HAS_OPTIONAL:
                optionCount = stream.readU30()
                if optionCount == 0:
                    raise Exception("optionCount is 0")

                for n in range(optionCount):
                    param = meth.params[len(meth.params) - optionCount + n]
                    val = stream.readU30()
                    kind = stream.readU8()

                    param.default = self.__getValue(kind, val)
                    

            if meth.flags & MethodFlags.HAS_PARAM_NAMES:
                for n in range(paramCount):
                    meth.params[n].name = self.getString(stream.readU30())
                    

    def __readMetadataInfo(self, stream: ABCInputStream) -> None:
        metadataCount = stream.readU30()
        self.metadata = []

        for _ in range(metadataCount):
            name = self.getString(stream.readU30())
            assert name is not None
            metadata = Metadata(name)

            itemCount = stream.readU30()
            for _ in range(itemCount):
                key = self.getString(stream.readU30())
                value = self.getString(stream.readU30())
                metadata.items.append(MetadataItem(key, value))

            self.metadata.append(metadata)


    def __readClassInfo(self, stream: ABCInputStream) -> None:
        self.__classes.clear()

        classCount = stream.readU30()

        for n in range(classCount):
            name = self.getMultiname(stream.readU30())
            if type(name) != QName:
                raise Exception("expected QName for instance name")

            superName = self.getMultiname(stream.readU30())
            if superName is not None and not isinstance(superName, QName):
                raise Exception("super name is not a QName")

            cls = Class(name)
            cls.superName = superName

            
            flags = stream.readU8()
            cls.sealed = bool(flags & 0x01) # CONSTANT_ClassSealed
            cls.final = bool(flags & 0x02) # CONSTANT_ClassFinal
            cls.interface = bool(flags & 0x04) # CONSTANT_Interface

            if flags & 0x08: # CONSTANT_ClassProtectedNs
                ns = self.getNamespace(stream.readU30())
                if ns is None:
                    raise Exception("protected ns is None")

                cls.protectedNs = ns

            interfaceCount = stream.readU30()
            for _ in range(interfaceCount):
                interface = self.getMultiname(stream.readU30())
                if not isinstance(interface, Multiname):
                    raise Exception("interface is not a Multiname")

                cls.interfaces.append(interface)

            cls.iinit = self.getMethod(stream.readU30())

            traitCount = stream.readU30()
            for _ in range(traitCount):
                cls.itraits.append(self.__readTrait(stream))

            self.__classes.append(cls)


        for n in range(classCount):
            cls = self.getClass(n)
            cls.cinit = self.getMethod(stream.readU30())

            traitCount = stream.readU30()
            for _ in range(traitCount):
                cls.ctraits.append(self.__readTrait(stream))


    def __readScriptInfo(self, stream: ABCInputStream) -> None:
        self.scripts = []

        scriptCount = stream.readU30()
        for _ in range(scriptCount):
            script = Script()
            script.init = self.getMethod(stream.readU30())
            
            traitCount = stream.readU30()
            for _ in range(traitCount):
                script.traits.append(self.__readTrait(stream))
            
            self.scripts.append(script)


    def __readMethodBodyInfo(self, stream: ABCInputStream) -> None:
        methodBodyCount = stream.readU30()
        
        for _ in range(methodBodyCount):
            method = self.getMethod(stream.readU30())
            
            if method.body:
                raise Exception("method already has a body")

            maxStack = stream.readU30()
            localCount = stream.readU30()
            initScopeDepth = stream.readU30()
            maxScopeDepth = stream.readU30()
            code = stream.read(stream.readU30())

            # store our exceptions and targets (for exceptions)
            exceptions = []
            targets: dict[int, ABCTarget] = {}

            # read exceptions
            exceptionCount = stream.readU30()
            for _ in range(exceptionCount):
                # read positions
                from_ = stream.readU30()
                to = stream.readU30()
                target = stream.readU30()

                # read exc info
                excType = self.getMultiname(stream.readU30())
                varName = self.getMultiname(stream.readU30())

                # create our targets
                targets[from_] = targets.get(from_, ABCTarget(from_))
                targets[to] = targets.get(to, ABCTarget(to))
                targets[target] = targets.get(target, ABCTarget(target))

                # create our exception and store it
                exception = ABCException(targets[from_], targets[to], targets[target], excType, varName)
                exceptions.append(exception)
                
            # disassemble
            bytecode = ABCBytecode.disassemble(code, self, targets)

            # create our body
            body = MethodBody(maxStack, localCount, initScopeDepth, maxScopeDepth, bytecode)
            body.exceptions = exceptions

            traitCount = stream.readU30()
            for _ in range(traitCount):
                body.traits.append(self.__readTrait(stream))

            # store the body in our method
            method.body = body
            


    def __getValue(self, kind: int, val: int) -> ValueType:
        if kind not in (0x0B, 0x0A, 0x0C, 0x00) and val == 0:
            raise Exception("getting value of 0")

        if kind == 0x0B: # CONSTANT_True
            return True

        elif kind == 0x0A: # CONSTANT_False
            return False

        elif kind == 0x0C: # CONSTANT_Null
            return Null

        elif kind == 0x00: # CONSTANT_Undefined
            return Undefined

        elif kind == 0x03: # CONSTANT_Int
            return self.getInteger(val) # type: ignore

        elif kind == 0x04: # CONSTANT_UInt
            return self.getUInteger(val) # type: ignore

        elif kind == 0x06: # CONSTANT_Double
            return self.getDouble(val) # type: ignore

        elif kind == 0x01: # CONSTANT_Utf8
            return self.getString(val) # type: ignore

        elif kind in NamespaceDict:
            ns: BaseNamespace = self.getNamespace(val) # type: ignore
            if ns.kind != kind:
                raise Exception("bad ns kind %d - expected %d" % (kind, ns.kind))
            
            return ns

        else:
            raise Exception("not supported kind %02x" % kind)



    def __readTrait(self, stream: ABCInputStream) -> Trait:
        name = self.getMultiname(stream.readU30())
        if type(name) != QName:
            raise Exception("Trait name is not a QName")
            print("name", name)
            
        kind = stream.readU8()
        attr, kind = kind >> 4, kind & 15

        final = bool(attr & 0x01)
        override = bool(attr & 0x02)

        traitType = TraitDict[kind]
        trait: Trait

        if (final or override) and not issubclass(traitType, TraitMethod):
            raise Exception("final or override shouldn't be set")

        if issubclass(traitType, TraitSlot):
            slotId = stream.readU30()
            typeValue = self.getMultiname(stream.readU30())
            if typeValue is not None and not isinstance(typeValue, (QName, TypeName)):
                raise Exception("type value is %r" % typeValue)

            value: ValueType = Undefined
            
            vindex = stream.readU30()
            if vindex:
                vkind = stream.readU8()
                value = self.__getValue(vkind, vindex)

            trait = traitType(name, slotId, typeValue, value)

        elif issubclass(traitType, TraitClass):
            slotId = stream.readU30()
            classi = self.getClass(stream.readU30())
            
            trait = traitType(name, slotId, classi)

        elif issubclass(traitType, TraitFunction):
            slotId = stream.readU30()
            function = self.getMethod(stream.readU30())

            trait = traitType(name, slotId, function)

        elif issubclass(traitType, TraitMethod):
            dispId = stream.readU30()
            method = self.getMethod(stream.readU30())

            trait = traitType(name, dispId, method, final, override)

        else:
            raise Exception("can't read %r" % traitType)

        
        if attr & 0x04: # ATTR_Metadata
            metadataCount = stream.readU30()
            trait.metadata = [
                self.metadata[stream.readU30()]
                for _ in range(metadataCount)
            ]

        return trait
    

    def export(self) -> bytes:
        exporter = ABCExporter(self)
        res = exporter.export()
        return res 