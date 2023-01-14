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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, TypeVar
    from swf.abc.ValueType import ValueType

    T = TypeVar("T")

class ABCFile:
    minorVersion: int
    majorVersion: int
    metadata: list[Metadata]
    scripts: list[Script]
    
    # constant pool
    _integerPool: list[int | None]
    _uintegerPool: list[int | None]
    _doublePool: list[float | None]
    _stringPool: list[str | None]
    _namespacePool: list[BaseNamespace | None]
    _nsSetPool: list[list[BaseNamespace] | None]
    _multinamePool: list[BaseMultiname | None]

    # also other pools
    _methods: list[Method]
    _classes: list[Class]

    def __init__(self, data: bytes | None = None) -> None:
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


    def export(self) -> bytes:
        print(".. generating pools ..")
        self.__generatePools()
        
        print(".. writing ..")
        stream = ABCOutputStream()
        stream.writeU16(self.minorVersion)
        stream.writeU16(self.majorVersion)
        self.__writeConstantPool(stream)
        self.__writeMethodInfo(stream)
        self.__writeMetadataInfo(stream)
        self.__writeClassInfo(stream)
        self.__writeScriptInfo(stream)
        self.__writeMethodBodyInfo(stream)
        return stream.getBytes()


    def __generatePools(self) -> None:
        self._integerPool = [None]
        self._uintegerPool = [None]
        self._doublePool = [None]
        self._stringPool = [None]
        self._namespacePool = [None]
        self._nsSetPool = [None]
        self._multinamePool = [None]
        
        self._methods = []
        self._classes = []

        queue: list[Any] = []

        for script in self.scripts:
            self.__populatePools(script.init)
            self.__populatePools(*script.traits)


    def __addToPool(self, pool: list[T], value: T) -> bool:
        if type(value) not in (str, int, float, list) and hasattr(value, "_cache"):
            return True
            
        if value in pool:
            return True

        if type(value) not in (str, int, float, list):
            value._cache = True # type: ignore

        pool.append(value)
        return False


    def __addValueToPool(self, vtype: BaseMultiname | None, value: ValueType | None) -> None:
        if type(value) == int:
            # we consider everything an int, unless
            # the type is explictly an uint
            if False and isinstance(vtype, QName) and vtype.name == "uint":
                self.__addToPool(self._uintegerPool, value)
            else:
                self.__addToPool(self._integerPool, value)

        elif type(value) == float:
            self.__addToPool(self._doublePool, value)

        elif type(value) == str:
            self.__addToPool(self._stringPool, value)

        elif isinstance(value, (BaseMultiname, BaseNamespace)):
            self.__populatePools(value)

        elif type(value) == bool or value in (Null, Undefined, None):
            pass

        else:
            raise NotImplementedError(type(value))


    def __populatePools(self, *elems: Any) -> None:
        for elem in elems:
            if isinstance(elem, Class):
                if self.__addToPool(self._classes, elem):
                    continue

                self.__populatePools(
                    elem.name, elem.superName, *elem.interfaces,
                    elem.cinit, elem.iinit,
                    *elem.ctraits, *elem.itraits,
                    elem.protectedNs)

            elif isinstance(elem, Method):
                for param in elem.params:
                    self.__populatePools(param.type)
                    self.__addToPool(self._stringPool, param.name)
                    self.__addValueToPool(param.type, param.default)

                self.__populatePools(elem.returnType)
                self.__addToPool(self._stringPool, elem.name)

                self.__addToPool(self._methods, elem)

                if elem.body:
                    for exc in elem.body.exceptions:
                        self.__populatePools(exc.excType, exc.varName)
                        
                    self.__populatePools(*elem.body.traits)

                    for instr in elem.body.bytecode.code:
                        if not isinstance(instr, ABCInstruction):
                            continue
                        
                        info = Instructions[instr.name]

                        for index, arg in enumerate(info.args):
                            value = instr.args[index]
                            if arg == Argument.Int:
                                assert type(value) == int
                                self.__addToPool(self._integerPool, value)

                            elif arg == Argument.UInt:
                                assert type(value) == int
                                self.__addToPool(self._uintegerPool, value)

                            elif arg == Argument.Double:
                                assert type(value) == float
                                self.__addToPool(self._doublePool, value)

                            elif arg == Argument.String:
                                assert type(value) == str
                                self.__addToPool(self._stringPool, value)

                            elif arg in (Argument.Namespace, Argument.Multiname, Argument.Class, Argument.Method):
                                self.__populatePools(value)

            elif isinstance(elem, Trait):
                self.__populatePools(elem.name)

                if isinstance(elem, TraitClass):
                    self.__populatePools(elem.classi)

                elif isinstance(elem, TraitFunction):
                    self.__populatePools(elem.function)

                elif isinstance(elem, TraitMethod):
                    self.__populatePools(elem.method)

                elif isinstance(elem, TraitSlot):
                    self.__populatePools(elem.type)
                    self.__addValueToPool(elem.type, elem.value)

                else:
                    raise NotImplementedError(elem)

            elif isinstance(elem, BaseNamespace):
                self.__addToPool(self._stringPool, elem.name)
                self.__addToPool(self._namespacePool, elem)

            elif isinstance(elem, BaseMultiname):
                if isinstance(elem, QName):
                    self.__addToPool(self._stringPool, elem.name)
                    self.__populatePools(elem.ns)

                elif isinstance(elem, Multiname):
                    self.__addToPool(self._stringPool, elem.name)
                    self.__addToPool(self._nsSetPool, elem.nsSet)
                    self.__populatePools(*elem.nsSet)

                elif isinstance(elem, MultinameL):
                    self.__addToPool(self._nsSetPool, elem.nsSet)
                    self.__populatePools(*elem.nsSet)

                elif isinstance(elem, RTQName):
                    self.__addToPool(self._stringPool, elem.name)
                    
                elif isinstance(elem, RTQNameL):
                    pass

                elif isinstance(elem, TypeName):
                    self.__populatePools(elem.qname, *elem.params)

                else:
                    raise NotImplementedError(elem)

                self.__addToPool(self._multinamePool, elem)

            elif elem is None:
                pass

            else:
                raise NotImplementedError(type(elem))


    def __readConstantPool(self, stream: ABCInputStream) -> None:
        self._integerPool = [None]
        self._uintegerPool = [None]
        self._doublePool = [None]
        self._stringPool = [None]
        self._namespacePool = [None]
        self._nsSetPool = [None]
        self._multinamePool = [None]


        intCount = stream.readU30()
        for _ in range(1, intCount):
            self._integerPool.append(stream.readS32())


        uintCount = stream.readU30()
        for _ in range(1, uintCount):
            self._uintegerPool.append(stream.readU32())


        doubleCount = stream.readU30()
        for _ in range(1, doubleCount):
            self._doublePool.append(stream.readD64())


        stringCount = stream.readU30()
        for _ in range(1, stringCount):
            self._stringPool.append(stream.read(stream.readU30()).decode("utf8"))


        namespaceCount = stream.readU30()
        for _ in range(1, namespaceCount):
            nsType = NamespaceDict[stream.readU8()]
            name = self._stringPool[stream.readU30()]
            self._namespacePool.append(nsType(name))


        nsSet: list[BaseNamespace] | None
        nsSetCount = stream.readU30()
        for _ in range(1, nsSetCount):
            count = stream.readU30()
            nsSet = []
            for _ in range(count):
                ns = self._namespacePool[stream.readU30()]
                assert ns is not None

                nsSet.append(ns)

            self._nsSetPool.append(nsSet)


        multinameCount = stream.readU30()
        for _ in range(1, multinameCount):
            multinameType = MultinameDict[stream.readU8()]

            if issubclass(multinameType, QName):
                ns = self._namespacePool[stream.readU30()]
                name = self._stringPool[stream.readU30()]
                self._multinamePool.append(multinameType(ns, name))

            elif issubclass(multinameType, RTQName):
                name = self._stringPool[stream.readU30()]
                self._multinamePool.append(multinameType(name))

            elif issubclass(multinameType, RTQNameL):
                self._multinamePool.append(multinameType())

            elif issubclass(multinameType, Multiname):
                name = self._stringPool[stream.readU30()]
                nsSet = self._nsSetPool[stream.readU30()]
                if nsSet is None:
                    raise Exception("nsSet cannot be None")

                self._multinamePool.append(multinameType(name, nsSet))

            elif issubclass(multinameType, MultinameL):
                nsSet = self._nsSetPool[stream.readU30()]
                if nsSet is None:
                    raise Exception("nsSet cannot be None")

                self._multinamePool.append(multinameType(nsSet))

            elif issubclass(multinameType, TypeName):
                qname = self._multinamePool[stream.readU30()]
                if type(qname) != QName:
                    raise Exception("expected QName")

                # avmplus apparently only supports count of 1
                count = stream.readU30()
                if count != 1:
                    raise Exception("count must be 1")

                param = self._multinamePool[stream.readU30()]

                # TODO: this might be allowed actually
                if param is None:
                    raise Exception("param can't be None")
                    
                self._multinamePool.append(multinameType(qname, [param]))

            else:
                raise Exception("Can't read %s" % type)

    
    def __readMethodInfo(self, stream: ABCInputStream) -> None:
        self._methods = []

        methodCount = stream.readU30()
        for _ in range(methodCount):
            meth = Method()
            self._methods.append(meth)

            paramCount = stream.readU30()
            returnType = self._multinamePool[stream.readU30()]
            if returnType is not None and not isinstance(returnType, (QName, TypeName)):
                raise Exception("return type is not a QName or TypeName (%r)" % returnType)

            meth.returnType = returnType

            for _ in range(paramCount):
                paramType = self._multinamePool[stream.readU30()]
                if paramType is not None and not isinstance(paramType, (QName, TypeName)):
                    raise Exception("param type is not a QName or TypeName")         

                param = Param(paramType)
                meth.params.append(param)

            meth.name = self._stringPool[stream.readU30()]
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
                    meth.params[n].name = self._stringPool[stream.readU30()]


    def __readMetadataInfo(self, stream: ABCInputStream) -> None:
        metadataCount = stream.readU30()
        self.metadata = []

        for _ in range(metadataCount):
            name = self._stringPool[stream.readU30()]
            assert name is not None
            metadata = Metadata(name)

            itemCount = stream.readU30()
            for _ in range(itemCount):
                key = self._stringPool[stream.readU30()]
                value = self._stringPool[stream.readU30()]
                metadata.items.append(MetadataItem(key, value))

            self.metadata.append(metadata)

    def __readClassInfo(self, stream: ABCInputStream) -> None:
        self._classes = []

        classCount = stream.readU30()

        for n in range(classCount):
            name = self._multinamePool[stream.readU30()]
            if type(name) != QName:
                raise Exception("expected QName for instance name")

            superName = self._multinamePool[stream.readU30()]
            if superName is not None and not isinstance(superName, QName):
                raise Exception("super name is not a QName")

            cls = Class(name)
            cls.superName = superName

            
            flags = stream.readU8()
            cls.sealed = bool(flags & 0x01) # CONSTANT_ClassSealed
            cls.final = bool(flags & 0x02) # CONSTANT_ClassFinal
            cls.interface = bool(flags & 0x04) # CONSTANT_Interface

            if flags & 0x08: # CONSTANT_ClassProtectedNs
                ns = self._namespacePool[stream.readU30()]
                if ns is None:
                    raise Exception("protected ns is None")

                cls.protectedNs = ns

            interfaceCount = stream.readU30()
            for _ in range(interfaceCount):
                interface = self._multinamePool[stream.readU30()]
                if not isinstance(interface, Multiname):
                    raise Exception("interface is not a Multiname")

                cls.interfaces.append(interface)

            cls.iinit = self._methods[stream.readU30()]

            traitCount = stream.readU30()
            for _ in range(traitCount):
                cls.itraits.append(self.__readTrait(stream))

            self._classes.append(cls)


        for n in range(classCount):
            cls = self._classes[n]
            cls.cinit = self._methods[stream.readU30()]

            traitCount = stream.readU30()
            for _ in range(traitCount):
                cls.ctraits.append(self.__readTrait(stream))


    def __readScriptInfo(self, stream: ABCInputStream) -> None:
        self.scripts = []

        scriptCount = stream.readU30()
        for _ in range(scriptCount):
            script = Script()
            script.init = self._methods[stream.readU30()]
            
            traitCount = stream.readU30()
            for _ in range(traitCount):
                script.traits.append(self.__readTrait(stream))

            self.scripts.append(script)


    def __readMethodBodyInfo(self, stream: ABCInputStream) -> None:
        methodBodyCount = stream.readU30()
        
        for _ in range(methodBodyCount):
            method = self._methods[stream.readU30()]
            
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
                excType = self._multinamePool[stream.readU30()]
                varName = self._multinamePool[stream.readU30()]

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
            return self._integerPool[val] # type: ignore

        elif kind == 0x04: # CONSTANT_UInt
            return self._uintegerPool[val] # type: ignore

        elif kind == 0x06: # CONSTANT_Double
            return self._doublePool[val] # type: ignore

        elif kind == 0x01: # CONSTANT_Utf8
            return self._stringPool[val] # type: ignore

        elif kind in NamespaceDict:
            ns: BaseNamespace = self._namespacePool[val] # type: ignore
            if ns.kind != kind:
                raise Exception("bad ns kind %d - expected %d" % (kind, ns.kind))
            
            return ns

        else:
            raise Exception("not supported kind %02x" % kind)


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
                return 0x04, self._uintegerPool.index(value)
            else:
                return 0x03, self._integerPool.index(value)

        elif type(value) == float:
            return 0x06, self._doublePool.index(value)

        elif type(value) == str:
            return 0x01, self._stringPool.index(value)

        elif isinstance(value, BaseNamespace):
            return value.kind, self._namespacePool.index(value)

        else:
            raise Exception("not supported value %r" % value)


    def __readTrait(self, stream: ABCInputStream) -> Trait:
        name = self._multinamePool[stream.readU30()]
        if type(name) != QName:
            #raise Exception("Trait name is not a QName")
            #print("name", name)
            pass # temporary
            
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
            typeValue = self._multinamePool[stream.readU30()]
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
            classi = self._classes[stream.readU30()]
            
            trait = traitType(name, slotId, classi)

        elif issubclass(traitType, TraitFunction):
            slotId = stream.readU30()
            function = self._methods[stream.readU30()]

            trait = traitType(name, slotId, function)

        elif issubclass(traitType, TraitMethod):
            dispId = stream.readU30()
            method = self._methods[stream.readU30()]

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


    def __writeConstantPool(self, stream: ABCOutputStream) -> None:
        stream.writeU30(len(self._integerPool))
        for integer in self._integerPool[1:]:
            assert integer is not None
            stream.writeS32(integer)

        stream.writeU30(len(self._uintegerPool))
        for uinteger in self._uintegerPool[1:]:
            assert uinteger is not None
            stream.writeU32(uinteger)

        stream.writeU30(len(self._doublePool))
        for double in self._doublePool[1:]:
            assert double is not None
            stream.writeD64(double)

        stream.writeU30(len(self._stringPool))
        for string in self._stringPool[1:]:
            assert string is not None
            utf8 = string.encode("utf8")
            stream.writeU30(len(utf8))
            stream.write(utf8)

        stream.writeU30(len(self._namespacePool))
        for namespace in self._namespacePool[1:]:
            assert namespace is not None
            stream.writeU8(namespace.kind)
            stream.writeU30(self._stringPool.index(namespace.name))

        stream.writeU30(len(self._nsSetPool))
        for nsSet in self._nsSetPool[1:]:
            assert nsSet is not None
            stream.writeU30(len(nsSet))
            for namespace in nsSet:
                stream.writeU30(self._namespacePool.index(namespace))

        stream.writeU30(len(self._multinamePool))
        for multiname in self._multinamePool[1:]:
            assert multiname is not None
            stream.writeU8(multiname.kind)

            if isinstance(multiname, QName):
                stream.writeU30(self._namespacePool.index(multiname.ns))
                stream.writeU30(self._stringPool.index(multiname.name))

            elif isinstance(multiname, RTQName):
                stream.writeU30(self._stringPool.index(multiname.name))

            elif isinstance(multiname, RTQNameL):
                pass

            elif isinstance(multiname, Multiname):
                stream.writeU30(self._stringPool.index(multiname.name))
                stream.writeU30(self._nsSetPool.index(multiname.nsSet))

            elif isinstance(multiname, MultinameL):
                stream.writeU30(self._nsSetPool.index(multiname.nsSet))

            elif isinstance(multiname, TypeName):
                assert len(multiname.params) == 1
                stream.writeU30(self._multinamePool.index(multiname.qname))
                stream.writeU30(len(multiname.params))
                stream.writeU30(self._multinamePool.index(multiname.params[0]))

            else:
                raise NotImplementedError(multiname)




    def __writeMethodInfo(self, stream: ABCOutputStream) -> None:
        stream.writeU30(len(self._methods))
        for method in self._methods:
            stream.writeU30(len(method.params))
            stream.writeU30(self._multinamePool.index(method.returnType))
            for param in method.params:
                stream.writeU30(self._multinamePool.index(param.type))

            stream.writeU30(self._stringPool.index(method.name))

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
                    stream.writeU30(self._stringPool.index(param.name))

    
    def __writeMetadataInfo(self, stream: ABCOutputStream) -> None:
        if len(self.metadata) != 0:
            raise NotImplementedError("metadata")
            
        stream.writeU30(0)


    def __writeClassInfo(self, stream: ABCOutputStream) -> None:
        stream.writeU30(len(self._classes))

        for cls in self._classes:
            stream.writeU30(self._multinamePool.index(cls.name))
            stream.writeU30(self._multinamePool.index(cls.superName))
            
            flags = 0
            if cls.sealed: flags |= 0x01
            if cls.final: flags |= 0x02
            if cls.interface: flags |= 0x04
            if cls.protectedNs is not None: flags |= 0x08

            stream.writeU8(flags)
            
            if cls.protectedNs is not None:
                stream.writeU30(self._namespacePool.index(cls.protectedNs))

            stream.writeU30(len(cls.interfaces))
            for interface in cls.interfaces:
                stream.writeU30(self._multinamePool.index(interface))

            stream.writeU30(self._methods.index(cls.iinit))
            
            stream.writeU30(len(cls.itraits))
            for trait in cls.itraits:
                self.__writeTrait(stream, trait)

        for cls in self._classes:
            stream.writeU30(self._methods.index(cls.cinit))
            
            stream.writeU30(len(cls.ctraits))
            for trait in cls.ctraits:
                self.__writeTrait(stream, trait)


    def __writeScriptInfo(self, stream: ABCOutputStream) -> None:
        stream.writeU30(len(self.scripts))

        for script in self.scripts:
            stream.writeU30(self._methods.index(script.init))
            
            stream.writeU30(len(script.traits))
            for trait in script.traits:
                self.__writeTrait(stream, trait)


    def __writeMethodBodyInfo(self, stream: ABCOutputStream) -> None:
        count = 0
        for method in self._methods:
            if method.body:
                count += 1

        stream.writeU30(count)

        for idx, method in enumerate(self._methods):
            if method.body:
                stream.writeU30(idx)
                stream.writeU30(method.body.maxStack)
                stream.writeU30(method.body.localCount)
                stream.writeU30(method.body.initScopeDepth)
                stream.writeU30(method.body.maxScopeDepth)

                code = method.body.bytecode.assemble(self)
                stream.writeU30(len(code))
                stream.write(code)

                stream.writeU30(len(method.body.exceptions))
                for exc in method.body.exceptions:
                    assert method.body.bytecode.targets is not None
                    stream.writeU30(method.body.bytecode.targets[exc.from_.id])
                    stream.writeU30(method.body.bytecode.targets[exc.to.id])
                    stream.writeU30(method.body.bytecode.targets[exc.target.id])
                    stream.writeU30(self._multinamePool.index(exc.excType))
                    stream.writeU30(self._multinamePool.index(exc.varName))

                stream.writeU30(len(method.body.traits))
                for trait in method.body.traits:
                    self.__writeTrait(stream, trait)


    def __writeTrait(self, stream: ABCOutputStream, trait: Trait) -> None:
        stream.writeU30(self._multinamePool.index(trait.name))

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
            stream.writeU30(self._multinamePool.index(trait.type))
            
            kind, value = self.__getKindVal(trait.type, trait.value)
            stream.writeU30(value)
            if value:
                stream.writeU8(kind)

        elif isinstance(trait, TraitClass):
            stream.writeU30(trait.slotId)
            stream.writeU30(self._classes.index(trait.classi))

        elif isinstance(trait, TraitMethod):
            stream.writeU30(trait.dispId)
            stream.writeU30(self._methods.index(trait.method))

        if trait.metadata is not None:
            stream.writeU30(len(trait.metadata))
            for metadata in trait.metadata:
                stream.writeU30(self.metadata.index(metadata))