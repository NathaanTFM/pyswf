from __future__ import annotations
from .BaseMultiname import BaseMultiname
from .Multiname import Multiname
from .MultinameA import MultinameA
from .MultinameL import MultinameL
from .MultinameLA import MultinameLA
from .QName import QName
from .QNameA import QNameA
from .RTQName import RTQName
from .RTQNameA import RTQNameA
from .RTQNameL import RTQNameL
from .RTQNameLA import RTQNameLA
from .TypeName import TypeName

MultinameDict: dict[int, type[BaseMultiname]] = {
    QName.kind: QName,
    QNameA.kind: QNameA,
    RTQName.kind: RTQName,
    RTQNameA.kind: RTQNameA,
    RTQNameL.kind: RTQNameL,
    RTQNameLA.kind: RTQNameLA,
    Multiname.kind: Multiname,
    MultinameA.kind: MultinameA,
    MultinameL.kind: MultinameL,
    MultinameLA.kind: MultinameLA,
    TypeName.kind: TypeName
}

__all__ = [
    'BaseMultiname',
    'Multiname', 'MultinameA',
    'MultinameL', 'MultinameLA',
    'QName', 'QNameA',
    'RTQName', 'RTQNameA',
    'RTQNameL', 'RTQNameLA',
    'TypeName',
    'MultinameDict'
]