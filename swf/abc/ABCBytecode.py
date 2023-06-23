from __future__ import annotations
from swf.abc.ABCInputStream import ABCInputStream
from swf.abc.ABCOutputStream import ABCOutputStream
from swf.abc.Class import Class
from swf.abc.Instructions import Argument, Instructions, Opcodes
from swf.abc.Method import Method
from swf.abc.multinames.BaseMultiname import BaseMultiname
from swf.abc.namespaces.BaseNamespace import BaseNamespace

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from swf.abc.ABCFile import ABCFile
    from swf.abc.ABCExporter import ABCExporter



class ABCTarget(int):
    id: int

    def __init__(self, id: int) -> None:
        self.id = id


    def __eq__(self, other: Any) -> bool:
        return type(other) == ABCTarget and other.id == self.id


    def __repr__(self) -> str:
        return "ABCTarget(%d)" % self.id


#ArgType = Union[int, str, float, BaseNamespace, BaseMultiname, Class, Method, ABCTarget, None]
ArgType = Any


class ABCInstruction:
    name: str
    args: list[ArgType]

    def __init__(self, name: str, args: list[ArgType]):
        self.name = name
        self.args = args


    def __repr__(self) -> str:
        return "ABCInstruction(%r, %r)" % (self.name, self.args)


class ABCBytecode:
    code: list[ABCInstruction | ABCTarget]
    targets: dict[int, int] | None = None

    def __init__(self, code: list[ABCInstruction | ABCTarget] | None = None):
        self.code = code if code is not None else []
        self.targets = None


    def dump(self) -> None:
        for elem in self.code:
            if isinstance(elem, ABCInstruction):
                print(" " + elem.name.ljust(20, " ") + ", ".join(str(arg) for arg in elem.args))

            elif isinstance(elem, ABCTarget):
                print("@%d" % elem.id)


    def emit(self, name: str, *args: ArgType) -> None:
        self.code.append(ABCInstruction(name, list(args)))


    def target(self, id: int) -> ABCTarget:
        target = ABCTarget(id)
        self.code.append(target)
        return target


    def assemble(self, exporter: ABCExporter) -> bytes:
        # target id to binary pos
        self.targets = {}

        # positions of targets to fill
        # (target id => (pos, relpos))
        positions: dict[int, list[tuple[int, int]]] = {}

        # stream
        stream = ABCOutputStream()

        for elem in self.code:
            position = stream.length()

            if type(elem) == ABCInstruction:
                info = Instructions[elem.name]
                stream.writeU8(info.opcode)

                if info.name == "lookupswitch":
                    for idx, value in enumerate(elem.args):
                        assert isinstance(value, ABCTarget)
                        if value.id in self.targets:
                            stream.writeS24(self.targets[value.id] - position)

                        else:
                            pos = stream.length()
                            stream.writeS24(0)
                            if not value.id in positions:
                                positions[value.id] = []

                            positions[value.id].append((pos, position))

                        if idx == 0:
                            stream.writeU30(len(elem.args) - 2)

                    continue


                for index, arg in enumerate(info.args):
                    value = elem.args[index]
                    if arg == Argument.U30:
                        stream.writeU30(value)

                    elif arg == Argument.Byte:
                        assert type(value) == int
                        stream.writeS8(value)

                    elif arg == Argument.Short:
                        assert type(value) == int
                        assert -32768 <= value <= 32767
                        stream.writeS32(value)
                        
                    elif arg == Argument.Int:
                        assert type(value) == int
                        stream.writeU30(exporter.getIntegerIndex(value))
                        
                    elif arg == Argument.UInt:
                        assert type(value) == int
                        stream.writeU30(exporter.getUIntegerIndex(value))
                        
                    elif arg == Argument.Double:
                        assert type(value) == float
                        stream.writeU30(exporter.getDoubleIndex(value))
                        
                    elif arg == Argument.String:
                        assert type(value) == str
                        stream.writeU30(exporter.getStringIndex(value))

                    elif arg == Argument.Namespace:
                        assert isinstance(value, BaseNamespace)
                        stream.writeU30(exporter.getNamespaceIndex(value))

                    elif arg == Argument.Multiname:
                        assert isinstance(value, BaseMultiname)
                        stream.writeU30(exporter.getMultinameIndex(value))

                    elif arg == Argument.Class:
                        assert type(value) == Class
                        stream.writeU30(exporter.getClassIndex(value))

                    elif arg == Argument.Method:
                        assert type(value) == Method
                        stream.writeU30(exporter.getMethodIndex(value))

                    elif arg == Argument.Target:
                        assert type(value) == ABCTarget
                        if value.id in self.targets:
                            stream.writeS24(self.targets[value.id] - (position + 4))

                        else:
                            pos = stream.length()
                            stream.writeS24(0)
                            if not value.id in positions:
                                positions[value.id] = []

                            positions[value.id].append((pos, position + 4))

                    elif arg == Argument.Exception:
                        assert type(value) == int
                        stream.writeU30(value)

                    else:
                        raise NotImplementedError(arg)


            elif type(elem) == ABCTarget:
                self.targets[elem.id] = position

                if elem.id in positions:
                    for pos, relpos in positions[elem.id]:
                        stream.writeS24(position - relpos, pos)

                    del positions[elem.id]

        if positions:
            raise Exception("Unresolved targets! (%r)" % positions.keys())

        return stream.getBytes()


    @staticmethod
    def disassemble(bytecode: bytes, abc: ABCFile, targets: dict[int, ABCTarget] | None = None) -> ABCBytecode:
        stream = ABCInputStream(bytecode)

        code: list[ABCInstruction | ABCTarget] = []

        # binary pos to target
        if targets is None:
            targets = {}

        # binary pos to list pos (indices)
        positions: dict[int, int] = {}

        while stream.available():
            position = stream.position()
            positions[position] = len(code)

            opcode = stream.readU8()
            info = Opcodes[opcode]
            args: list[ArgType] = []

            if info.name == "lookupswitch":
                target = stream.readS24() + position
                if target not in targets:
                    targets[target] = ABCTarget(target)

                args.append(targets[target])

                caseCount = stream.readU30() + 1
                for _ in range(caseCount):
                    caseTarget = stream.readS24() + position
                    if caseTarget not in targets:
                        targets[caseTarget] = ABCTarget(caseTarget)

                    args.append(targets[caseTarget])

                continue

            for arg in info.args:
                if arg == Argument.U30:
                    args.append(stream.readU30())

                elif arg == Argument.Byte:
                    args.append(stream.readS8())

                elif arg == Argument.Short:
                    # it's technically a U30 but it's easier for us
                    # to handle it as a S32
                    val = stream.readS32()
                    assert -32768 <= val <= 32767
                    args.append(val)

                elif arg == Argument.Int:
                    args.append(abc.getInteger(stream.readU30()))

                elif arg == Argument.UInt:
                    args.append(abc.getUInteger(stream.readU30()))

                elif arg == Argument.Double:
                    args.append(abc.getDouble(stream.readU30()))

                elif arg == Argument.String:
                    args.append(abc.getString(stream.readU30()))

                elif arg == Argument.Namespace:
                    args.append(abc.getNamespace(stream.readU30()))

                elif arg == Argument.Multiname:
                    args.append(abc.getMultiname(stream.readU30()))

                elif arg == Argument.Class:
                    args.append(abc.getClass(stream.readU30()))

                elif arg == Argument.Method:
                    args.append(abc.getMethod(stream.readU30()))

                elif arg == Argument.Target:
                    target = stream.readS24() + position + 4

                    # apparently if AVM2 jumps outside, it just does not jump
                    if target >= len(bytecode):
                        target = position + 4

                    if target not in targets:
                        targets[target] = ABCTarget(target)

                    args.append(targets[target])

                elif arg == Argument.Exception:
                    args.append(stream.readU30())

                else:
                    raise NotImplementedError(arg)

            instruction = ABCInstruction(info.name, args)
            code.append(instruction)

        # add targets
        for pos in sorted(targets.keys(), reverse = True):
            index = positions[pos]
            code.insert(index, targets[pos])

        return ABCBytecode(code)