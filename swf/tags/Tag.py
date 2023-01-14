from __future__ import annotations
from typing import ClassVar
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class Tag:
    tagId: ClassVar[int]

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        raise NotImplementedError()
        
    
    def write(self, stream: SWFOutputStream) -> None:
        raise NotImplementedError()