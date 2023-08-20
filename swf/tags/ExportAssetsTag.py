from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ExportAssetsTag(Tag):
    """
    The ExportAssets tag makes portions of a
    SWF file available for import by other SWF files.
    """
    tagId = 56

    characters: list[tuple[int, str]]

    def __init__(self, characters: list[tuple[int, str]]):
        self.characters = characters


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 5:
            raise ValueError("bad swf version")

        characters = []
        count = stream.readUI16()
        for _ in range(count):
            tag = stream.readUI16()
            name = stream.readString()
            characters.append((tag, name))

        return ExportAssetsTag(characters)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 5:
            raise ValueError("bad swf version")

        stream.writeUI16(len(self.characters))
        for tag, name in self.characters:
            stream.writeUI16(tag)
            stream.writeString(name)