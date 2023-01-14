from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class DefineSceneAndFrameLabelDataTag(Tag):
    """
    The DefineSceneAndFrameLabelData tag contains scene and
    frame label data for a MovieClip.
    """
    tagId = 86

    scenes: list[tuple[int, str]]
    labels: list[tuple[int, str]]

    def __init__(self, scenes: list[tuple[int, str]], labels: list[tuple[int, str]]):
        self.scenes = scenes
        self.labels = labels


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        if stream.version < 9:
            raise ValueError("bad swf version")

        scenes = []
        sceneCount = stream.readEncodedU32()
        for _ in range(sceneCount):
            offset = stream.readEncodedU32()
            name = stream.readString()
            scenes.append((offset, name))

        labels = []
        frameLabelCount = stream.readEncodedU32()
        for _ in range(frameLabelCount):
            frameNum = stream.readEncodedU32()
            frameLabel = stream.readString()
            labels.append((frameNum, frameLabel))

        return DefineSceneAndFrameLabelDataTag(scenes, labels)



    def write(self, stream: SWFOutputStream) -> None:
        if stream.version < 9:
            raise ValueError("bad swf version")

        stream.writeEncodedU32(len(self.scenes))
        for offset, name in self.scenes:
            stream.writeEncodedU32(offset)
            stream.writeString(name)
            
        stream.writeEncodedU32(len(self.labels))
        for frameNum, frameLabel in self.labels:
            stream.writeEncodedU32(frameNum)
            stream.writeString(frameLabel)