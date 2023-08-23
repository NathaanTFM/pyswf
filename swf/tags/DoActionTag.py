from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.stream.ActionStream import ActionStream
from swf.actions.ActionRecord import ActionRecord

class DoActionTag(Tag):
    """
    DoAction instructs Flash Player to perform a list of actions
    when the current frame is complete.
    """
    tagId = 12

    actions: list[ActionRecord]

    def __init__(self, actions: list[ActionRecord]) -> None:
        self.actions = actions


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 6:
            raise ValueError("bad swf version")
        
        actions = []
        while 1:
            action = ActionStream.readAction(stream)
            if action is None:
                break

            actions.append(action)

        return DoActionTag(actions)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 6:
            raise ValueError("bad swf version")

        for action in self.actions:
            ActionStream.writeAction(stream, action)

        stream.writeUI8(0)