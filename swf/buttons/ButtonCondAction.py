from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.stream.ActionStream import ActionStream

class ButtonCondAction:
    idleToOverDown: bool
    outDownToIdle: bool
    outDownToOverDown: bool
    overDownToOutDown: bool
    overDownToOverUp: bool
    overUpToOverDown: bool
    overUpToIdle: bool
    idleToOverUp: bool
    keyPress: int
    overDownToIdle: bool
    actions: list[ActionRecord]

    def __init__(self, idleToOverDown: bool, outDownToIdle: bool, outDownToOverDown: bool, overDownToOutDown: bool, overDownToOverUp: bool, overUpToOverDown: bool, overUpToIdle: bool, idleToOverUp: bool, keyPress: int, overDownToIdle: bool, actions: list[ActionRecord]):
        self.idleToOverDown = idleToOverDown
        self.outDownToIdle = outDownToIdle
        self.outDownToOverDown = outDownToOverDown
        self.overDownToOutDown = overDownToOutDown
        self.overDownToOverUp = overDownToOverUp
        self.overUpToOverDown = overUpToOverDown
        self.overUpToIdle = overUpToIdle
        self.idleToOverUp = idleToOverUp
        self.keyPress = keyPress
        self.overDownToIdle = overDownToIdle
        self.actions = actions
        

    @staticmethod
    def read(stream: SWFInputStream) -> ButtonCondAction:
        condActionSize = stream.readUI16()

        idleToOverDown = stream.readUB1()
        outDownToIdle = stream.readUB1()
        outDownToOverDown = stream.readUB1()
        overDownToOutDown = stream.readUB1()
        overDownToOverUp = stream.readUB1()
        overUpToOverDown = stream.readUB1()
        overUpToIdle = stream.readUB1()
        idleToOverUp = stream.readUB1()
        keyPress = stream.readUB(7)
        overDownToIdle = stream.readUB1()

        actions = []
        while 1:
            action = ActionStream.readAction(stream)
            if action is None:
                break

            actions.append(action)

        return ButtonCondAction(idleToOverDown, outDownToIdle, outDownToOverDown, overDownToOutDown, overDownToOverUp, overUpToOverDown, overUpToIdle, idleToOverUp, keyPress, overDownToIdle, actions)
    

    def write(self, stream: SWFOutputStream, isLast: bool) -> None:
        strm2 = SWFOutputStream(stream.version)

        strm2.writeUB1(self.idleToOverDown)
        strm2.writeUB1(self.outDownToIdle)
        strm2.writeUB1(self.outDownToOverDown)
        strm2.writeUB1(self.overDownToOutDown)
        strm2.writeUB1(self.overDownToOverUp)
        strm2.writeUB1(self.overUpToOverDown)
        strm2.writeUB1(self.overUpToIdle)
        strm2.writeUB1(self.idleToOverUp)
        strm2.writeUB(7, self.keyPress)
        strm2.writeUB1(self.overDownToIdle)

        for action in self.actions:
            ActionStream.writeAction(strm2, action)

        strm2.writeUI8(0)

        # write to stream
        stream.writeUI16(0 if isLast else strm2.getLength() + 2)
        stream.write(strm2.getBytes())