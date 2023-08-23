from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ImportAssets2Tag(Tag):
    """
    The ImportAssets2 tag replaces the ImportAssets tag for SWF 8 and later.
    ImportAssets2 currently mirrors the ImportAssets tag's functionality
    """
    tagId = 71

    url: str
    characters: list[tuple[int, str]]

    def __init__(self, url: str, characters: list[tuple[int, str]]) -> None:
        self.url = url
        self.characters = characters


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 8:
            raise ValueError("bad swf version")
        
        url = stream.readString()
        if stream.readUI8() != 1: # downloadNow
            raise Exception("reserved is not 1")
        
        if stream.readUI8() != 0: # hasDigest
            raise Exception("reserved is not 0")
        
        count = stream.readUI16()
        characters: list[tuple[int, str]] = []
        
        for _ in range(count):
            tag = stream.readUI16()
            name = stream.readString()
            characters.append((tag, name))

        return ImportAssets2Tag(url, characters)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 8:
            raise ValueError("bad swf version")
        
        stream.writeString(self.url)
        stream.writeUI8(1)
        stream.writeUI8(0)

        stream.writeUI16(len(self.characters))
        for tag, name in self.characters:
            stream.writeUI16(tag)
            stream.writeString(name)