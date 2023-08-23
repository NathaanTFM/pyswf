from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class ImportAssetsTag(Tag):
    """
    The ImportAssets tag imports characters from another SWF file.
    The importing SWF file references the exporting SWF file by the URL where it can be found.
    Imported assets are added to the dictionary just like characters defined within a SWF file
    """
    tagId = 57

    url: str
    characters: list[tuple[int, str]]

    def __init__(self, url: str, characters: list[tuple[int, str]]) -> None:
        self.url = url
        self.characters = characters


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 5:
            raise ValueError("bad swf version")
        
        url = stream.readString()
        
        count = stream.readUI16()
        characters: list[tuple[int, str]] = []
        
        for _ in range(count):
            tag = stream.readUI16()
            name = stream.readString()
            characters.append((tag, name))

        return ImportAssetsTag(url, characters)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 5:
            raise ValueError("bad swf version")
        
        stream.writeString(self.url)

        stream.writeUI16(len(self.characters))
        for tag, name in self.characters:
            stream.writeUI16(tag)
            stream.writeString(name)