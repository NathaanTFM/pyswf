from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class SymbolClassTag(Tag):
    """
    The SymbolClass tag creates associations between
    symbols in the SWF file and ActionScript 3.0 classes.
    It is the ActionScript 3.0 equivalent of the
    ExportAssets tag.
    """
    tagId = 76

    symbols: list[tuple[int, str]]

    def __init__(self, symbols: list[tuple[int, str]]):
        self.symbols = symbols


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 9:
            raise ValueError("bad swf version")

        symbols = []
        numSymbols = stream.readUI16()

        for _ in range(numSymbols):
            tag = stream.readUI16()
            name = stream.readString()
            symbols.append((tag, name))

        return SymbolClassTag(symbols)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 9:
            raise ValueError("bad swf version")

        stream.writeUI16(len(self.symbols))
        
        for tag, name in self.symbols:
            stream.writeUI16(tag)
            stream.writeString(name)