from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.stream.ActionStream import ActionStream
from swf.buttons.ButtonRecord import ButtonRecord
from swf.buttons.ButtonCondAction import ButtonCondAction

class DefineButton2Tag(Tag):
    """
    The ShowFrame tag instructs Flash Player to display the
    contents of the display list. The file is paused for
    the duration of a single frame.
    """
    tagId = 34

    buttonId: int
    trackAsMenu: bool
    characters: list[ButtonRecord]
    actions: list[ButtonCondAction] | None

    def __init__(self, buttonId: int, trackAsMenu: bool, characters: list[ButtonRecord], actions: list[ButtonCondAction] | None):
        self.buttonId = buttonId
        self.trackAsMenu = trackAsMenu
        self.characters = characters
        self.actions = actions


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 3:
            raise ValueError("bad swf version")
        
        buttonId = stream.readUI16()
        if stream.readUB(7) != 0:
            raise Exception("reserved is non-zero")
        
        trackAsMenu = stream.readUB1()
        actionOffset = stream.readUI16() # should we check it?
        
        characters = []
        while 1:
            record = ButtonRecord.read(stream, 2)
            if record is None:
                break

            characters.append(record)

        actions = None
        if actionOffset != 0:
            actions = []
            while stream.available():
                action = ButtonCondAction.read(stream)
                actions.append(action)

        return DefineButton2Tag(buttonId, trackAsMenu, characters, actions)
    

    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 3:
            raise ValueError("bad swf version")
        
        stream.writeUI16(self.buttonId)
        stream.writeUB(7, 0)
        stream.writeUB1(self.trackAsMenu)
        
        # make new stream
        strm2 = SWFOutputStream(stream.version)
        for record in self.characters:
            record.write(strm2, 2)

        strm2.writeUI8(0)

        # back to stream
        stream.writeUI16(0 if self.actions is None else strm2.getLength() + 2)
        stream.write(strm2.getBytes())

        if self.actions is not None:
            for index, action in enumerate(self.actions):
                action.write(stream, index == len(self.actions)-1)
                