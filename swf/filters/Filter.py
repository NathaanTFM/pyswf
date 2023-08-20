from __future__ import annotations
from typing import ClassVar

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class Filter:
    id: ClassVar[int]

    @staticmethod
    def read(stream: SWFInputStream) -> Filter:
        raise NotImplementedError()
    

    def write(self, stream: SWFOutputStream) -> None:
        raise NotImplementedError()