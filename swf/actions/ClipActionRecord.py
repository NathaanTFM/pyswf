from __future__ import annotations
from swf.enums.ClipEventFlags import ClipEventFlags
from swf.stream.ActionStream import ActionStream
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ClipActionRecord:
    eventFlags: ClipEventFlags
    keyCode: int | None
    actions: list[ActionRecord]

    def __init__(self, eventFlags: ClipEventFlags, keyCode: int | None, actions: list[ActionRecord]) -> None:
        self.eventFlags = eventFlags
        self.keyCode = keyCode
        self.actions = actions

    
    @staticmethod
    def readArray(stream: SWFInputStream) -> list[ClipActionRecord]:
        res = []

        if stream.readUI16() != 0:
            raise Exception("reserved is set")

        allEventFlags = ClipEventFlags.read(stream)
        allEventFlagsCheck = ClipEventFlags(0)
        while True:
            eventFlags = ClipEventFlags.read(stream)
            if not eventFlags:
                break

            allEventFlagsCheck |= eventFlags

            actionRecordSize = stream.readUI32() # TODO

            keyCode = None
            if eventFlags & ClipEventFlags.KEY_PRESS:
                keyCode = stream.readUI8()
            
            #actionRecords = stream.read(actionRecordSize)
            actions = []
            while 1:
                action = ActionStream.readAction(stream)
                if not action:
                    break

                actions.append(action)

            res.append(ClipActionRecord(eventFlags, keyCode, actions))
        
        if allEventFlags != allEventFlagsCheck:
            raise Exception("all event flags is wrong")

        return res
    

    @staticmethod
    def writeArray(stream: SWFOutputStream, array: list[ClipActionRecord]) -> None:
        stream.writeUI16(0)

        allEventFlags = ClipEventFlags(0)
        for record in array:
            allEventFlags |= record.eventFlags


        allEventFlags.write(stream)
        
        for elem in array:
            elem.eventFlags.write(stream)
            if not elem.eventFlags:
                raise Exception("event flags is zero")
            
            # another stream
            strm2 = SWFOutputStream(stream.version)

            if elem.eventFlags & ClipEventFlags.KEY_PRESS:
                assert elem.keyCode is not None
                strm2.writeUI8(elem.keyCode)

            for action in elem.actions:
                ActionStream.writeAction(strm2, action)

            strm2.writeUI8(0)

            # back to stream
            stream.writeUI32(strm2.getLength())
            stream.write(strm2.getBytes())

        ClipEventFlags(0).write(stream)