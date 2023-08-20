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
    notImplemented: set[str] = set()

    @staticmethod
    def readTag(stream: SWFInputStream, interestedSet: set[int] | None = None) -> Tag:
        """
        Read a Tag
        """
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
            if DEBUGGING:
                tag._tmp = tagData # type: ignore
                
            return tag

        # find tag class
        if tagCode >= len(TagDict):
            raise ValueError("tag %d not found" % tagCode)

        tagType = TagDict[tagCode]
        if tagType is None:
            raise ValueError("tag %d not found" % tagCode)
            
        if DEBUGGING:
            print("\n" * 3)
            print("Reading tag %r" % tagType.__name__)

        # create our tag
        try:
            tag = tagType.read(stream)
        except NotImplementedError:
            tag = None

        # check our tag
        if tag:
            if stream.available() > 1:
                print("data left (%d) after reading %s" % (stream.available(), tagType.__name__))

            if DEBUGGING:
                tag._tmp = tagData # type: ignore

        else:
            if tagType.__name__ not in TagStream.notImplemented:
                print("not implemented %s" % tagType.__name__)
                TagStream.notImplemented.add(tagType.__name__)
                
            tag = RawTag(tagCode, tagData)
            if DEBUGGING:
                tag._tmp = tagData # type: ignore
            
        return tag

    
    
    @staticmethod
    def writeTag(stream: SWFOutputStream, tag: Tag) -> None:
        # export tag
        if DEBUGGING:
            print("\n" * 3)
            print("Writing tag %r" % tag)

        tagStream = SWFOutputStream(stream.version)
        
        try:
            tag.write(tagStream)
        except Exception as e:
            print("Failed to write %r" % tag)
            raise
        
        data = tagStream.getBytes()

        # XXX ultra supra debugging mode
        if DEBUGGING:
            tmp: bytes = tag._tmp # type: ignore 

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
                print("\n" * 3)
                print("Attempt to read broken tag rn")
                type(tag).read(st)

        # tag header
        if len(data) < 0x3F:
            stream.writeUI16((tag.tagId << 6) | len(data))
        else:
            stream.writeUI16((tag.tagId << 6) | 0x3F)
            stream.writeUI32(len(data))

        # write bytes
        stream.write(data)