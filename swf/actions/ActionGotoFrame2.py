from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionGotoFrame2(ActionRecord):
    code = 0x9F

    def __init__(self) -> None:
        ...

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        raise NotImplementedError()
    
    
    def write(self, stream: SWFOutputStream) -> None:
        raise NotImplementedError()