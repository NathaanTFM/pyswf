from __future__ import annotations
from swf.tags.TagDict import TagDict
from swf.tags.Tag import Tag
from swf.tags.RawTag import RawTag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

from typing import TYPE_CHECKING
import os
DEBUGGING = int(os.environ.get("PYSWF_DEBUG", 0)) >= 1
if DEBUGGING:
    import sys

class TagStream:
    if DEBUGGING:
        debugTagCounter: int = 0

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
            
        if DEBUGGING:
            print("Reading tag %r" % tagType.__name__)
            SWFInputStream.debugBuffer = ""

        # create our tag
        try:
            tag = tagType.read(stream)

        except NotImplementedError:
            if tagType.__name__ not in TagStream.notImplemented:
                print("not implemented %s" % tagType.__name__)
                TagStream.notImplemented.add(tagType.__name__)
                
            tag = RawTag(tagCode, tagData)

        else:
            if stream.available() > 1:
                print("data left (%d) after reading %s" % (stream.available(), tagType.__name__))

        if DEBUGGING:
            tag._tmp = tagData # type: ignore
            tag._debug = SWFInputStream.debugBuffer # type: ignore
            tag._cnt = TagStream.debugTagCounter # type: ignore
            TagStream.debugTagCounter += 1

        return tag

    
    @staticmethod
    def writeTag(stream: SWFOutputStream, tag: Tag) -> None:
        # export tag
        if DEBUGGING:
            print("Writing tag %r" % tag)

        tagStream = SWFOutputStream(stream.version)
        
        try:
            tag.write(tagStream)
        except Exception as e:
            print("Failed to write %r" % tag)
            raise
        
        data = tagStream.getBytes()

        # XXX ultra supra debugging mode
        if DEBUGGING and hasattr(tag, "_tmp"):
            tmp: bytes = tag._tmp

            if data != tmp:
                print("[!!!] tag mismatch (%s)" % tag.__class__.__name__)
                print("      length %d (orig %d)" % (len(data), len(tmp)))

                if "-v" in sys.argv:
                    print("== New ==")
                    for n in range(0, len(data), 32):
                        print(data[n:n+32].hex(":", 1))

                    print("")
                    print("== Original ==")
                    for n in range(0, len(tmp), 32):
                        print(tmp[n:n+32].hex(":", 1))

                st = SWFInputStream(stream.version, data)
                SWFInputStream.debugBuffer = ""
                type(tag).read(st)

                filename = "mismatch_%r_%i" % (type(tag).__name__, tag._cnt) # type: ignore
                with open(filename + "_orig.txt", "w") as f:
                    f.write(tag._debug) # type: ignore
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