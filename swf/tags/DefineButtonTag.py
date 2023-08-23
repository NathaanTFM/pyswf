from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.stream.ActionStream import ActionStream
from swf.buttons.ButtonRecord import ButtonRecord
from swf.actions.ActionRecord import ActionRecord

class DefineButtonTag(Tag):
    """
    The ShowFrame tag instructs Flash Player to display the
    contents of the display list. The file is paused for
    the duration of a single frame.
    """
    tagId = 7

    buttonId: int
    characters: list[ButtonRecord]
    actions: list[ActionRecord]

    def __init__(self, buttonId: int, characters: list[ButtonRecord], actions: list[ActionRecord]):
        self.buttonId = buttonId
        self.characters = characters
        self.actions = actions


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")
        
        buttonId = stream.readUI16()
        characters = []
        while 1:
            record = ButtonRecord.read(stream, 1)
            if record is None:
                break

            characters.append(record)

        actions = []
        while 1:
            action = ActionStream.readAction(stream)
            if action is None:
                break

            actions.append(action)

        return DefineButtonTag(buttonId, characters, actions)
    

    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")
        
        raise NotImplementedError()