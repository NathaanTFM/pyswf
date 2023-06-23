from typing import Hashable
from swf.abc.Pool import Pool, T

class UniquePool(Pool[T]):
    def _getKey(self, elt: T) -> Hashable:
        return hash(elt)