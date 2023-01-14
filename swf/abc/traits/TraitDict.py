from __future__ import annotations
from .Trait import Trait
from .TraitSlot import TraitSlot
from .TraitMethod import TraitMethod
from .TraitGetter import TraitGetter
from .TraitSetter import TraitSetter
from .TraitClass import TraitClass
from .TraitFunction import TraitFunction
from .TraitConst import TraitConst

TraitDict: dict[int, type[Trait]] = {
    TraitSlot.kind: TraitSlot,
    TraitMethod.kind: TraitMethod,
    TraitGetter.kind: TraitGetter,
    TraitSetter.kind: TraitSetter,
    TraitClass.kind: TraitClass,
    TraitFunction.kind: TraitFunction,
    TraitConst.kind: TraitConst
}

__all__ = [
    'Trait',
    'TraitSlot',
    'TraitMethod',
    'TraitGetter',
    'TraitSetter',
    'TraitClass',
    'TraitFunction',
    'TraitConst',
    'TraitDict'
]