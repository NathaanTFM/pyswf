from __future__ import annotations
from typing import ClassVar, Any
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class Tag:
    tagId: ClassVar[int]

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        raise NotImplementedError()
        
    
    def write(self, stream: SWFOutputStream) -> None:
        raise NotImplementedError()
    

    def __hash__(self) -> int:
        return id(self)
    

    def __eq__(self, other: Any) -> bool:
        return self is other