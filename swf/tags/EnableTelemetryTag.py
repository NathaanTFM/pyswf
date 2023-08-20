from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class EnableTelemetryTag(Tag):
    """
    Telemetry is a a Flash player feature that sends profiling information about the runtime and the currently 
    running content. The EnableTelemetry tag controls whether the advanced features of telemetry are included in 
    the profile data. If the tag isn’t present, only basic information is available.
    """
    tagId = 93
    
    passwordHash: bytes | None
    
    def __init__(self, passwordHash: bytes | None = None):
        self.passwordHash = passwordHash
        

    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 1:
            raise ValueError("bad swf version")
            
        if stream.readUI16() != 0:
            raise Exception("reserved is non-zero")
            
        avail = stream.available()
        if avail == 0:
            passwordHash = None
        elif avail == 32:
            passwordHash = stream.read(32)
        else:
            raise Exception("bad length for hash (%d)" % avail)
            
        return EnableTelemetryTag(passwordHash)
            

    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 1:
            raise ValueError("bad swf version")
            
        stream.writeUI16(0)
        
        if self.passwordHash is not None:
            if len(self.passwordHash) != 32:
                raise Exception("bad length for hash (%d)" % len(self.passwordHash))
                
            stream.write(self.passwordHash)