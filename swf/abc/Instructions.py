from __future__ import annotations
import enum

__all__ = ["Instructions", "Opcodes", "InstructionList", "Argument"]

class Argument(enum.Enum):
    U30 = "u30"
    Byte = "byte"
    Short = "short"
    Int = "int"
    UInt = "uint"
    Double = "double"
    String = "string"
    Namespace = "namespace"
    Multiname = "multiname"
    Class = "class"
    Method = "method"
    Target = "target"
    Exception = "exception"


class InstructionInfo:
    name: str
    opcode: int
    args: tuple[Argument, ...]

    def __init__(self, name: str, opcode: int, *args: Argument) -> None:
        self.name = name
        self.opcode = opcode
        self.args = args


InstructionList: list[InstructionInfo] = [
    InstructionInfo("add", 0xA0),
    InstructionInfo("add_i", 0xC5),
    InstructionInfo("applytype", 0x53, Argument.U30),
    InstructionInfo("astype", 0x86, Argument.Multiname),
    InstructionInfo("astypelate", 0x87),
    InstructionInfo("bitand", 0xA8),
    InstructionInfo("bitnot", 0x97),
    InstructionInfo("bitor", 0xA9),
    InstructionInfo("bitxor", 0xAA),
    InstructionInfo("bkpt", 0x01),
    InstructionInfo("bkptline", 0xF2, Argument.U30),
    InstructionInfo("call", 0x41, Argument.U30),
    InstructionInfo("callmethod", 0x43, Argument.U30, Argument.U30),
    InstructionInfo("callproperty", 0x46, Argument.Multiname, Argument.U30),
    InstructionInfo("callproplex", 0x4C, Argument.Multiname, Argument.U30),
    InstructionInfo("callpropvoid", 0x4F, Argument.Multiname, Argument.U30),
    InstructionInfo("callstatic", 0x44, Argument.U30, Argument.U30),
    InstructionInfo("callsuper", 0x45, Argument.Multiname, Argument.U30),
    InstructionInfo("callsupervoid", 0x4E, Argument.Multiname, Argument.U30),
    InstructionInfo("checkfilter", 0x78),
    InstructionInfo("coerce", 0x80, Argument.Multiname),
    InstructionInfo("coerce_a", 0x82),
    InstructionInfo("coerce_b", 0x81),
    InstructionInfo("coerce_d", 0x84),
    InstructionInfo("coerce_i", 0x83),
    InstructionInfo("coerce_o", 0x89),
    InstructionInfo("coerce_s", 0x85),
    InstructionInfo("coerce_u", 0x88),
    InstructionInfo("construct", 0x42, Argument.U30),
    InstructionInfo("constructprop", 0x4A, Argument.Multiname, Argument.U30),
    InstructionInfo("constructsuper", 0x49, Argument.U30),
    InstructionInfo("convert_b", 0x76),
    InstructionInfo("convert_d", 0x75),
    InstructionInfo("convert_i", 0x73),
    InstructionInfo("convert_o", 0x77),
    InstructionInfo("convert_s", 0x70),
    InstructionInfo("convert_u", 0x74),
    InstructionInfo("debug", 0xEF, Argument.Byte, Argument.String, Argument.Byte, Argument.U30),
    InstructionInfo("debugfile", 0xF1, Argument.String),
    InstructionInfo("debugline", 0xF0, Argument.U30),
    InstructionInfo("declocal", 0x94, Argument.U30),
    InstructionInfo("declocal_i", 0xC3, Argument.U30),
    InstructionInfo("decrement", 0x93),
    InstructionInfo("decrement_i", 0xC1),
    InstructionInfo("deleteproperty", 0x6A, Argument.Multiname),
    InstructionInfo("divide", 0xA3),
    InstructionInfo("dup", 0x2A),
    InstructionInfo("dxns", 0x06, Argument.String),
    InstructionInfo("dxnslate", 0x07),
    InstructionInfo("equals", 0xAB),
    InstructionInfo("esc_xattr", 0x72),
    InstructionInfo("esc_xelem", 0x71),
    InstructionInfo("finddef", 0x5F, Argument.Multiname),
    InstructionInfo("findproperty", 0x5E, Argument.Multiname),
    InstructionInfo("findpropstrict", 0x5D, Argument.Multiname),
    InstructionInfo("getdescendants", 0x59, Argument.Multiname),
    InstructionInfo("getglobalscope", 0x64),
    InstructionInfo("getglobalslot", 0x6E, Argument.U30),
    InstructionInfo("getlex", 0x60, Argument.Multiname),
    InstructionInfo("getlocal", 0x62, Argument.U30),
    InstructionInfo("getlocal_0", 0xD0),
    InstructionInfo("getlocal_1", 0xD1),
    InstructionInfo("getlocal_2", 0xD2),
    InstructionInfo("getlocal_3", 0xD3),
    InstructionInfo("getouterscope", 0x67, Argument.U30),
    InstructionInfo("getproperty", 0x66, Argument.Multiname),
    InstructionInfo("getscopeobject", 0x65, Argument.U30),
    InstructionInfo("getslot", 0x6C, Argument.U30),
    InstructionInfo("getsuper", 0x04, Argument.Multiname),
    InstructionInfo("greaterequals", 0xB0),
    InstructionInfo("greaterthan", 0xAF),
    InstructionInfo("hasnext", 0x1F),
    InstructionInfo("hasnext2", 0x32, Argument.U30, Argument.U30),
    InstructionInfo("ifeq", 0x13, Argument.Target),
    InstructionInfo("iffalse", 0x12, Argument.Target),
    InstructionInfo("ifge", 0x18, Argument.Target),
    InstructionInfo("ifgt", 0x17, Argument.Target),
    InstructionInfo("ifle", 0x16, Argument.Target),
    InstructionInfo("iflt", 0x15, Argument.Target),
    InstructionInfo("ifne", 0x14, Argument.Target),
    InstructionInfo("ifnge", 0x0F, Argument.Target),
    InstructionInfo("ifngt", 0x0E, Argument.Target),
    InstructionInfo("ifnle", 0x0D, Argument.Target),
    InstructionInfo("ifnlt", 0x0C, Argument.Target),
    InstructionInfo("ifstricteq", 0x19, Argument.Target),
    InstructionInfo("ifstrictne", 0x1A, Argument.Target),
    InstructionInfo("iftrue", 0x11, Argument.Target),
    InstructionInfo("in", 0xB4),
    InstructionInfo("inclocal", 0x92, Argument.U30),
    InstructionInfo("inclocal_i", 0xC2, Argument.U30),
    InstructionInfo("increment", 0x91),
    InstructionInfo("increment_i", 0xC0),
    InstructionInfo("initproperty", 0x68, Argument.Multiname),
    InstructionInfo("instanceof", 0xB1),
    InstructionInfo("istype", 0xB2, Argument.Multiname),
    InstructionInfo("istypelate", 0xB3),
    InstructionInfo("jump", 0x10, Argument.Target),
    InstructionInfo("kill", 0x08, Argument.U30),
    InstructionInfo("label", 0x09),
    InstructionInfo("lessequals", 0xAE),
    InstructionInfo("lessthan", 0xAD),
    InstructionInfo("lf32", 0x38),
    InstructionInfo("lf64", 0x39),
    InstructionInfo("li16", 0x36),
    InstructionInfo("li32", 0x37),
    InstructionInfo("li8", 0x35),
    InstructionInfo("lookupswitch", 0x1B),
    InstructionInfo("lshift", 0xA5),
    InstructionInfo("modulo", 0xA4),
    InstructionInfo("multiply", 0xA2),
    InstructionInfo("multiply_i", 0xC7),
    InstructionInfo("negate", 0x90),
    InstructionInfo("negate_i", 0xC4),
    InstructionInfo("newactivation", 0x57),
    InstructionInfo("newarray", 0x56, Argument.U30),
    InstructionInfo("newcatch", 0x5A, Argument.Exception),
    InstructionInfo("newclass", 0x58, Argument.Class),
    InstructionInfo("newfunction", 0x40, Argument.Method),
    InstructionInfo("newobject", 0x55, Argument.U30),
    InstructionInfo("nextname", 0x1E),
    InstructionInfo("nextvalue", 0x23),
    InstructionInfo("nop", 0x02),
    InstructionInfo("not", 0x96),
    InstructionInfo("pop", 0x29),
    InstructionInfo("popscope", 0x1D),
    InstructionInfo("pushbyte", 0x24, Argument.Byte),
    InstructionInfo("pushdouble", 0x2F, Argument.Double),
    InstructionInfo("pushfalse", 0x27),
    InstructionInfo("pushint", 0x2D, Argument.Int),
    InstructionInfo("pushnamespace", 0x31, Argument.Namespace),
    InstructionInfo("pushnan", 0x28),
    InstructionInfo("pushnull", 0x20),
    InstructionInfo("pushscope", 0x30),
    InstructionInfo("pushshort", 0x25, Argument.Short),
    InstructionInfo("pushstring", 0x2C, Argument.String),
    InstructionInfo("pushtrue", 0x26),
    InstructionInfo("pushuint", 0x2E, Argument.UInt),
    InstructionInfo("pushundefined", 0x21),
    InstructionInfo("pushwith", 0x1C),
    InstructionInfo("returnvalue", 0x48),
    InstructionInfo("returnvoid", 0x47),
    InstructionInfo("rshift", 0xA6),
    InstructionInfo("setglobalslot", 0x6F, Argument.U30),
    InstructionInfo("setlocal", 0x63, Argument.U30),
    InstructionInfo("setlocal_0", 0xD4),
    InstructionInfo("setlocal_1", 0xD5),
    InstructionInfo("setlocal_2", 0xD6),
    InstructionInfo("setlocal_3", 0xD7),
    InstructionInfo("setproperty", 0x61, Argument.Multiname),
    InstructionInfo("setslot", 0x6D, Argument.U30),
    InstructionInfo("setsuper", 0x05, Argument.Multiname),
    InstructionInfo("sf32", 0x3D),
    InstructionInfo("sf64", 0x3E),
    InstructionInfo("si16", 0x3B),
    InstructionInfo("si32", 0x3C),
    InstructionInfo("si8", 0x3A),
    InstructionInfo("strictequals", 0xAC),
    InstructionInfo("subtract", 0xA1),
    InstructionInfo("subtract_i", 0xC6),
    InstructionInfo("swap", 0x2B),
    InstructionInfo("sxi1", 0x50),
    InstructionInfo("sxi16", 0x52),
    InstructionInfo("sxi8", 0x51),
    InstructionInfo("throw", 0x03),
    InstructionInfo("timestamp", 0xF3),
    InstructionInfo("typeof", 0x95),
    InstructionInfo("urshift", 0xA7)
]

Instructions: dict[str, InstructionInfo] = {}
for instr in InstructionList:
    Instructions[instr.name] = instr

Opcodes: dict[int, InstructionInfo] = {}
for instr in InstructionList:
    Opcodes[instr.opcode] = instr