from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.actions.ActionRecord import ActionRecord

from swf.actions.ActionNextFrame import ActionNextFrame
from swf.actions.ActionPreviousFrame import ActionPreviousFrame
from swf.actions.ActionPlay import ActionPlay
from swf.actions.ActionStop import ActionStop
from swf.actions.ActionToggleQuality import ActionToggleQuality
from swf.actions.ActionStopSounds import ActionStopSounds
from swf.actions.ActionAdd import ActionAdd
from swf.actions.ActionSubtract import ActionSubtract
from swf.actions.ActionMultiply import ActionMultiply
from swf.actions.ActionDivide import ActionDivide
from swf.actions.ActionEquals import ActionEquals
from swf.actions.ActionLess import ActionLess
from swf.actions.ActionAnd import ActionAnd
from swf.actions.ActionOr import ActionOr
from swf.actions.ActionNot import ActionNot
from swf.actions.ActionStringEquals import ActionStringEquals
from swf.actions.ActionStringLength import ActionStringLength
from swf.actions.ActionStringExtract import ActionStringExtract
from swf.actions.ActionPop import ActionPop
from swf.actions.ActionToInteger import ActionToInteger
from swf.actions.ActionGetVariable import ActionGetVariable
from swf.actions.ActionSetVariable import ActionSetVariable
from swf.actions.ActionSetTarget2 import ActionSetTarget2
from swf.actions.ActionStringAdd import ActionStringAdd
from swf.actions.ActionGetProperty import ActionGetProperty
from swf.actions.ActionSetProperty import ActionSetProperty
from swf.actions.ActionCloneSprite import ActionCloneSprite
from swf.actions.ActionRemoveSprite import ActionRemoveSprite
from swf.actions.ActionTrace import ActionTrace
from swf.actions.ActionStartDrag import ActionStartDrag
from swf.actions.ActionEndDrag import ActionEndDrag
from swf.actions.ActionStringLess import ActionStringLess
from swf.actions.ActionThrow import ActionThrow
from swf.actions.ActionCastOp import ActionCastOp
from swf.actions.ActionImplementsOp import ActionImplementsOp
from swf.actions.ActionRandomNumber import ActionRandomNumber
from swf.actions.ActionMBStringLength import ActionMBStringLength
from swf.actions.ActionCharToAscii import ActionCharToAscii
from swf.actions.ActionAsciiToChar import ActionAsciiToChar
from swf.actions.ActionGetTime import ActionGetTime
from swf.actions.ActionMBStringExtract import ActionMBStringExtract
from swf.actions.ActionMBCharToAscii import ActionMBCharToAscii
from swf.actions.ActionMBAsciiToChar import ActionMBAsciiToChar
from swf.actions.ActionDelete import ActionDelete
from swf.actions.ActionDelete2 import ActionDelete2
from swf.actions.ActionDefineLocal import ActionDefineLocal
from swf.actions.ActionCallFunction import ActionCallFunction
from swf.actions.ActionReturn import ActionReturn
from swf.actions.ActionModulo import ActionModulo
from swf.actions.ActionNewObject import ActionNewObject
from swf.actions.ActionDefineLocal2 import ActionDefineLocal2
from swf.actions.ActionInitArray import ActionInitArray
from swf.actions.ActionInitObject import ActionInitObject
from swf.actions.ActionTypeOf import ActionTypeOf
from swf.actions.ActionTargetPath import ActionTargetPath
from swf.actions.ActionEnumerate import ActionEnumerate
from swf.actions.ActionAdd2 import ActionAdd2
from swf.actions.ActionLess2 import ActionLess2
from swf.actions.ActionEquals2 import ActionEquals2
from swf.actions.ActionToNumber import ActionToNumber
from swf.actions.ActionToString import ActionToString
from swf.actions.ActionPushDuplicate import ActionPushDuplicate
from swf.actions.ActionStackSwap import ActionStackSwap
from swf.actions.ActionGetMember import ActionGetMember
from swf.actions.ActionSetMember import ActionSetMember
from swf.actions.ActionIncrement import ActionIncrement
from swf.actions.ActionDecrement import ActionDecrement
from swf.actions.ActionCallMethod import ActionCallMethod
from swf.actions.ActionNewMethod import ActionNewMethod
from swf.actions.ActionInstanceOf import ActionInstanceOf
from swf.actions.ActionEnumerate2 import ActionEnumerate2
from swf.actions.ActionBitAnd import ActionBitAnd
from swf.actions.ActionBitOr import ActionBitOr
from swf.actions.ActionBitXor import ActionBitXor
from swf.actions.ActionBitLShift import ActionBitLShift
from swf.actions.ActionBitRShift import ActionBitRShift
from swf.actions.ActionBitURShift import ActionBitURShift
from swf.actions.ActionStrictEquals import ActionStrictEquals
from swf.actions.ActionGreater import ActionGreater
from swf.actions.ActionStringGreater import ActionStringGreater
from swf.actions.ActionExtends import ActionExtends
from swf.actions.ActionGotoFrame import ActionGotoFrame
from swf.actions.ActionGetURL import ActionGetURL
from swf.actions.ActionStoreRegister import ActionStoreRegister
from swf.actions.ActionConstantPool import ActionConstantPool
from swf.actions.ActionWaitForFrame import ActionWaitForFrame
from swf.actions.ActionSetTarget import ActionSetTarget
from swf.actions.ActionGoToLabel import ActionGoToLabel
from swf.actions.ActionWaitForFrame2 import ActionWaitForFrame2
from swf.actions.ActionDefineFunction2 import ActionDefineFunction2
from swf.actions.ActionTry import ActionTry
from swf.actions.ActionWith import ActionWith
from swf.actions.ActionPush import ActionPush
from swf.actions.ActionJump import ActionJump
from swf.actions.ActionGetURL2 import ActionGetURL2
from swf.actions.ActionDefineFunction import ActionDefineFunction
from swf.actions.ActionIf import ActionIf
from swf.actions.ActionCall import ActionCall
from swf.actions.ActionGotoFrame2 import ActionGotoFrame2

ActionDict: dict[int, type[ActionRecord]] = {
    0x04: ActionNextFrame,
    0x05: ActionPreviousFrame,
    0x06: ActionPlay,
    0x07: ActionStop,
    0x08: ActionToggleQuality,
    0x09: ActionStopSounds,
    0x0A: ActionAdd,
    0x0B: ActionSubtract,
    0x0C: ActionMultiply,
    0x0D: ActionDivide,
    0x0E: ActionEquals,
    0x0F: ActionLess,
    0x10: ActionAnd,
    0x11: ActionOr,
    0x12: ActionNot,
    0x13: ActionStringEquals,
    0x14: ActionStringLength,
    0x15: ActionStringExtract,
    
    0x17: ActionPop,
    0x18: ActionToInteger,

    0x1C: ActionGetVariable,
    0x1D: ActionSetVariable,

    0x20: ActionSetTarget2,
    0x21: ActionStringAdd,
    0x22: ActionGetProperty,
    0x23: ActionSetProperty,
    0x24: ActionCloneSprite,
    0x25: ActionRemoveSprite,
    0x26: ActionTrace,
    0x27: ActionStartDrag,
    0x28: ActionEndDrag,
    0x29: ActionStringLess,
    0x2A: ActionThrow,
    0x2B: ActionCastOp,
    0x2C: ActionImplementsOp,

    0x30: ActionRandomNumber,
    0x31: ActionMBStringLength,
    0x32: ActionCharToAscii,
    0x33: ActionAsciiToChar,
    0x34: ActionGetTime,
    0x35: ActionMBStringExtract,
    0x36: ActionMBCharToAscii,
    0x37: ActionMBAsciiToChar,
    
    0x3A: ActionDelete,
    0x3B: ActionDelete2,
    0x3C: ActionDefineLocal,
    0x3D: ActionCallFunction,
    0x3E: ActionReturn,
    0x3F: ActionModulo,

    0x40: ActionNewObject,
    0x41: ActionDefineLocal2,
    0x42: ActionInitArray,
    0x43: ActionInitObject,
    0x44: ActionTypeOf,
    0x45: ActionTargetPath,
    0x46: ActionEnumerate,
    0x47: ActionAdd2,
    0x48: ActionLess2,
    0x49: ActionEquals2,
    0x4A: ActionToNumber,
    0x4B: ActionToString,
    0x4C: ActionPushDuplicate,
    0x4D: ActionStackSwap,
    0x4E: ActionGetMember,
    0x4F: ActionSetMember,
    0x50: ActionIncrement,
    0x51: ActionDecrement,
    0x52: ActionCallMethod,
    0x53: ActionNewMethod,
    0x54: ActionInstanceOf,
    0x55: ActionEnumerate2,

    0x60: ActionBitAnd,
    0x61: ActionBitOr,
    0x62: ActionBitXor,
    0x63: ActionBitLShift,
    0x64: ActionBitRShift,
    0x65: ActionBitURShift,
    0x66: ActionStrictEquals,
    0x67: ActionGreater,
    0x68: ActionStringGreater,
    0x69: ActionExtends,

    0x81: ActionGotoFrame,

    0x83: ActionGetURL,

    0x87: ActionStoreRegister,
    0x88: ActionConstantPool,

    0x8A: ActionWaitForFrame,
    0x8B: ActionSetTarget,
    0x8C: ActionGoToLabel,
    0x8D: ActionWaitForFrame2,
    0x8E: ActionDefineFunction2,
    0x8F: ActionTry,

    0x94: ActionWith,

    0x96: ActionPush,

    0x99: ActionJump,
    0x9A: ActionGetURL2,
    0x9B: ActionDefineFunction,
    0x9D: ActionIf,
    0x9E: ActionCall,
    0x9F: ActionGotoFrame2
}

__all__ = [
    "ActionNextFrame",
    "ActionPreviousFrame",
    "ActionPlay",
    "ActionStop",
    "ActionToggleQuality",
    "ActionStopSounds",
    "ActionAdd",
    "ActionSubtract",
    "ActionMultiply",
    "ActionDivide",
    "ActionEquals",
    "ActionLess",
    "ActionAnd",
    "ActionOr",
    "ActionNot",
    "ActionStringEquals",
    "ActionStringLength",
    "ActionStringExtract",
    "ActionPop",
    "ActionToInteger",
    "ActionGetVariable",
    "ActionSetVariable",
    "ActionSetTarget2",
    "ActionStringAdd",
    "ActionGetProperty",
    "ActionSetProperty",
    "ActionCloneSprite",
    "ActionRemoveSprite",
    "ActionTrace",
    "ActionStartDrag",
    "ActionEndDrag",
    "ActionStringLess",
    "ActionThrow",
    "ActionCastOp",
    "ActionImplementsOp",
    "ActionRandomNumber",
    "ActionMBStringLength",
    "ActionCharToAscii",
    "ActionAsciiToChar",
    "ActionGetTime",
    "ActionMBStringExtract",
    "ActionMBCharToAscii",
    "ActionMBAsciiToChar",
    "ActionDelete",
    "ActionDelete2",
    "ActionDefineLocal",
    "ActionCallFunction",
    "ActionReturn",
    "ActionModulo",
    "ActionNewObject",
    "ActionDefineLocal2",
    "ActionInitArray",
    "ActionInitObject",
    "ActionTypeOf",
    "ActionTargetPath",
    "ActionEnumerate",
    "ActionAdd2",
    "ActionLess2",
    "ActionEquals2",
    "ActionToNumber",
    "ActionToString",
    "ActionPushDuplicate",
    "ActionStackSwap",
    "ActionGetMember",
    "ActionSetMember",
    "ActionIncrement",
    "ActionDecrement",
    "ActionCallMethod",
    "ActionNewMethod",
    "ActionInstanceOf",
    "ActionEnumerate2",
    "ActionBitAnd",
    "ActionBitOr",
    "ActionBitXor",
    "ActionBitLShift",
    "ActionBitRShift",
    "ActionBitURShift",
    "ActionStrictEquals",
    "ActionGreater",
    "ActionStringGreater",
    "ActionExtends",
    "ActionGotoFrame",
    "ActionGetURL",
    "ActionStoreRegister",
    "ActionConstantPool",
    "ActionWaitForFrame",
    "ActionSetTarget",
    "ActionGoToLabel",
    "ActionWaitForFrame2",
    "ActionDefineFunction2",
    "ActionTry",
    "ActionWith",
    "ActionPush",
    "ActionJump",
    "ActionGetURL2",
    "ActionDefineFunction",
    "ActionIf",
    "ActionCall",
    "ActionGotoFrame2"
]