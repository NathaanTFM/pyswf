from __future__ import annotations
import enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swf.stream.SWFInputStream import SWFInputStream
    from swf.stream.SWFOutputStream import SWFOutputStream

class ClipEventFlags(enum.Flag):
    # byte 1
    KEY_UP = 0x80
    KEY_DOWN = 0x40
    MOUSE_UP = 0x20
    MOUSE_DOWN = 0x10
    MOUSE_MOVE = 0x08
    UNLOAD = 0x04
    ENTER_FRAME = 0x02
    LOAD = 0x01

    # byte 2
    DRAG_OVER = 0x8000
    ROLL_OUT = 0x4000
    ROLL_OVER = 0x2000
    RELEASE_OUTSIDE = 0x1000
    RELEASE = 0x800
    PRESS = 0x400
    INITIALIZE = 0x200
    DATA = 0x100

    # byte 3
    CONSTRUCT = 0x40000
    KEY_PRESS = 0x20000
    DRAG_OUT = 0x10000


    @staticmethod
    def read(stream: SWFInputStream) -> ClipEventFlags:
        if stream.version >= 6:
            clipEventFlags = ClipEventFlags(stream.readUI32())
        else:
            clipEventFlags = ClipEventFlags(stream.readUI16())

        if stream.version < 6 and clipEventFlags.value & 0xFF00:
            raise ValueError("bad swf version")

        if stream.version < 7 and clipEventFlags & ClipEventFlags.CONSTRUCT:
            raise ValueError("bad swf version")

        return clipEventFlags


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 6 and self.value & 0xFF00:
            raise ValueError("bad swf version")

        if stream.version < 7 and self & ClipEventFlags.CONSTRUCT:
            raise ValueError("bad swf version")

        if stream.version >= 6:
            stream.writeUI32(self.value)
        else:
            stream.writeUI16(self.value)