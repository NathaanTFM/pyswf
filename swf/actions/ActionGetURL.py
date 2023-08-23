from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionGetURL(ActionRecord):
    code = 0x83

    urlString: str
    targetString: str

    def __init__(self, urlString: str, targetString: str) -> None:
        self.urlString = urlString
        self.targetString = targetString

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        urlString = stream.readString()
        targetString = stream.readString()
        return ActionGetURL(urlString, targetString)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        stream.writeString(self.urlString)
        stream.writeString(self.targetString)