from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class MetadataTag(Tag):
    """
    The Metadata tag is an optional tag to describe 
    the SWF file to an external process.
    """
    tagId = 77

    metadata: str

    def __init__(self, metadata: str) -> None:
        self.metadata = metadata


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")

        metadata = stream.readString()
        return MetadataTag(metadata)
        

    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")

        stream.writeString(self.metadata)