from __future__ import annotations
from swf.actions.ActionDict import ActionDict
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.Debugging import Debugging

class ActionStream:
    notImplemented: set[str] = set()

    @staticmethod
    def readAction(stream: SWFInputStream) -> ActionRecord | None:
        actionCode = stream.readUI8()
        if actionCode == 0:
            return None
        
        cls = ActionDict[actionCode]

        if actionCode >= 0x80:
            length = stream.readUI16()
            data = SWFInputStream(stream.version, stream.read(length))
            try:
                action = cls.read(data)

            except NotImplementedError:
                Debugging.printVerbose("reading action %r is not implemented" % cls)
                action = ActionRecord()

            else:
                if data.available() > 0:
                    Debugging.printVerbose("data available after reading action %r" % cls)

        else:
            action = cls()
            
        return action
    
    
    @staticmethod
    def writeAction(stream: SWFOutputStream, action: ActionRecord) -> None:
        stream.writeUI8(action.code)

        if action.code >= 0x80:
            data = SWFOutputStream(stream.version)
            action.write(data)
            
            stream.writeUI16(data.getLength())
            stream.write(data.getBytes())
            