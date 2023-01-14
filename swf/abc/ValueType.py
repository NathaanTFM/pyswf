from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from swf.abc.constants.Null import NullType
    from swf.abc.constants.Undefined import UndefinedType
    from swf.abc.multinames.BaseMultiname import BaseMultiname
    from swf.abc.namespaces.BaseNamespace import BaseNamespace
    from typing import Union

    ValueType = Union[int, float, bool, str, NullType, UndefinedType, BaseMultiname, BaseNamespace]