from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.stream.ActionStream import ActionStream
from swf.actions.ActionRecord import ActionRecord

class DoInitActionTag(Tag):
    """
    The DoInitAction tag is similar to the DoAction tag: it defines a series of bytecodes
    to be executed. However, the actions defined with DoInitAction are executed earlier
    than the usual DoAction actions, and are executed only once.
    """
    tagId = 59

    spriteId: int
    actions: list[ActionRecord]

    def __init__(self, spriteId: int, actions: list[ActionRecord]) -> None:
        self.spriteId = spriteId
        self.actions = actions


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 6:
            raise ValueError("bad swf version")
        
        spriteId = stream.readUI16()

        actions = []
        while 1:
            action = ActionStream.readAction(stream)
            if action is None:
                break

            actions.append(action)

        return DoInitActionTag(spriteId, actions)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 6:
            raise ValueError("bad swf version")
        
        stream.writeUI16(self.spriteId)

        for action in self.actions:
            ActionStream.writeAction(stream, action)

        stream.writeUI8(0)