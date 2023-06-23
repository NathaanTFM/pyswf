from typing import Hashable, TypeVar
from swf.abc.Pool import Pool

T = TypeVar('T')

class ConstantPool(Pool[T]):
    def _getKey(self, elt: T) -> Hashable:
        return elt