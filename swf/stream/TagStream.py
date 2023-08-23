from __future__ import annotations
from swf.tags.TagDict import TagDict
from swf.tags.Tag import Tag
from swf.tags.RawTag import RawTag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream
from swf.Debugging import Debugging
import sys

class TagStream:
    if Debugging.enableTagCounter():
        debugTagCounter: int = 0

    if Debugging.showNotImplemented():
        notImplemented: set[str] = set()

    @staticmethod
    def readTag(stream: SWFInputStream, interestedSet: set[int] | None = None) -> Tag:
        """
        Read a Tag
        """
        tag: Tag # some typing to make mypy happy

        # read tag header
        tagCodeAndLength = stream.readUI16()
        tagCode = tagCodeAndLength >> 6
        tagLength = tagCodeAndLength & 0x3F

        if tagLength == 0x3F:
            tagLength = stream.readUI32()

        # read our tag data
        tagData = stream.read(tagLength)
        stream = SWFInputStream(stream.version, tagData)

        # check if we're interested in this tag, if not, just skip
        if interestedSet is not None and tagCode not in interestedSet:
            tag = RawTag(tagCode, tagData)
            return tag

        # find tag class
        if tagCode >= len(TagDict):
            raise ValueError("tag %d not found" % tagCode)

        tagType = TagDict[tagCode]
        if tagType is None:
            raise ValueError("tag %d not found" % tagCode)
            
        Debugging.printVerbose("Reading tag %r" % tagType.__name__)

        if Debugging.enableStreamVerbose():
            SWFInputStream.debugBuffer = ""

        # create our tag
        try:
            tag = tagType.read(stream)

        except NotImplementedError:
            if Debugging.showNotImplemented():
                if tagType.__name__ not in TagStream.notImplemented:
                    Debugging.printVerbose("missing tag implemented %s" % tagType.__name__)
                    TagStream.notImplemented.add(tagType.__name__)
                
            tag = RawTag(tagCode, tagData)

        else:
            if stream.available() > 1:
                Debugging.printVerbose("data left (%d) after reading %s" % (stream.available(), tagType.__name__))

        if Debugging.enableRawTag():
            tag._raw = tagData # type: ignore

        if Debugging.enableTagCounter():
            tag._cnt = TagStream.debugTagCounter # type: ignore
            TagStream.debugTagCounter += 1

        if Debugging.enableStreamVerbose():
            tag._verb = SWFInputStream.debugBuffer # type: ignore


        return tag

    
    @staticmethod
    def writeTag(stream: SWFOutputStream, tag: Tag) -> None:
        # export tag
        Debugging.printVerbose("Writing tag %r" % tag)

        tagStream = SWFOutputStream(stream.version)
        
        try:
            tag.write(tagStream)
        except Exception as e:
            print("Failed to write %r" % tag, file=sys.stderr)
            raise
        
        data = tagStream.getBytes()

        # XXX ultra supra debugging mode
        if Debugging.enableRawTag():
            tmp: bytes = tag._raw # type: ignore

            if data != tmp:
                Debugging.printVerbose("[!!!] tag mismatch (%s)" % tag.__class__.__name__)
                Debugging.printVerbose("      length %d (orig %d)" % (len(data), len(tmp)))

                if "-v" in sys.argv:
                    Debugging.printVerbose("== New ==")
                    for n in range(0, len(data), 32):
                        Debugging.printVerbose(data[n:n+32].hex(":", 1))

                    Debugging.printVerbose("")
                    Debugging.printVerbose("== Original ==")
                    for n in range(0, len(tmp), 32):
                        Debugging.printVerbose(tmp[n:n+32].hex(":", 1))

                if Debugging.enableStreamVerbose():
                    st = SWFInputStream(stream.version, data)
                    SWFInputStream.debugBuffer = ""
                    type(tag).read(st)

                    filename = "mismatch_%r_%i" % (type(tag).__name__, getattr(tag, "_cnt", __import__("random").randint(1000, 9999)))
                    with open(filename + "_orig.txt", "w") as f:
                        f.write(tag._verb) # type: ignore
                    with open(filename + "_new.txt", "w") as f:
                        f.write(SWFInputStream.debugBuffer)

        # tag header
        if len(data) < 0x3F:
            stream.writeUI16((tag.tagId << 6) | len(data))
        else:
            stream.writeUI16((tag.tagId << 6) | 0x3F)
            stream.writeUI32(len(data))

        # write bytes
        stream.write(data)