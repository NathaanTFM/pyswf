from __future__ import annotations
from typing import ClassVar

from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionRecord:
    code: ClassVar[int]

    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        raise NotImplementedError()
    
    
    def write(self, stream: SWFOutputStream) -> None:
        raise NotImplementedError()