from __future__ import annotations
from swf.actions.ActionRecord import ActionRecord
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ActionPush(ActionRecord):
    code = 0x96

    values: list[int | tuple[int, int | str | float | bool | None]]

    def __init__(self, values: list[int | tuple[int, int | str | float | bool | None]]):
        self.values = values

    
    @staticmethod
    def read(stream: SWFInputStream) -> ActionRecord:
        values: list[int | tuple[int, int | str | float | bool | None]] = []

        while stream.available():
            type = stream.readUI8()
            value: int | str | float | bool | None = None

            if type == 0:
                value = stream.readString()
            elif type == 1:
                value = stream.readFLOAT()
            elif type == 4:
                value = stream.readUI8()
            elif type == 5:
                value = bool(stream.readUI8())
            elif type == 6:
                value = stream.readDOUBLE()
            elif type == 7:
                value = stream.readUI32()
            elif type == 8:
                value = stream.readUI8()
            elif type == 9:
                value = stream.readUI16()

            if value is None:
                values.append(type)
            else:
                values.append((type, value))

        return ActionPush(values)
    
    
    def write(self, stream: SWFOutputStream) -> None:
        for element in self.values:
            if isinstance(element, int):
                type = element
                value = None
            else:
                type = element[0]
                value = element[1]

            stream.writeUI8(type)
            if type == 0:
                assert isinstance(value, str)
                stream.writeString(value)

            elif type == 1:
                assert isinstance(value, float)
                stream.writeFLOAT(value)

            elif type == 4:
                assert isinstance(value, int)
                stream.writeUI8(value)

            elif type == 5:
                assert isinstance(value, bool)
                stream.writeUI8(int(value))

            elif type == 6:
                assert isinstance(value, float)
                stream.writeDOUBLE(value)

            elif type == 7:
                assert isinstance(value, int)
                stream.writeUI32(value)
                
            elif type == 8:
                assert isinstance(value, int)
                stream.writeUI8(value)
                
            elif type == 9:
                assert isinstance(value, int)
                stream.writeUI16(value)
                
            else:
                assert value is None