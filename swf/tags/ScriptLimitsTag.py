from __future__ import annotations
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream

class ScriptLimitsTag(Tag):
    """
    The ScriptLimits tag includse two fields that can be used
    to override the default settings for maximum recursion depth
    and ActionsScript time-out.
    """
    tagId = 65

    maxRecursionDepth: int
    scriptTimeoutSeconds: int

    def __init__(self, maxRecursionDepth: int, scriptTimeoutSeconds: int) -> None:
        self.maxRecursionDepth = maxRecursionDepth
        self.scriptTimeoutSeconds = scriptTimeoutSeconds


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 7:
            raise ValueError("bad swf version")

        maxRecursionDepth = stream.readUI16()
        scriptTimeoutSeconds = stream.readUI16()
        return ScriptLimitsTag(maxRecursionDepth, scriptTimeoutSeconds)


    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 7:
            raise ValueError("bad swf version")

        stream.writeUI16(self.maxRecursionDepth)
        stream.writeUI16(self.scriptTimeoutSeconds)