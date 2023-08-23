from __future__ import annotations
from swf.tags.Tag import Tag
from swf.stream.SWFInputStream import SWFInputStream
from swf.stream.SWFOutputStream import SWFOutputStream

class VideoFrameTag(Tag):
    """
    VideoFrame provides a single frame of video data
    for a video character that is already defined with 
    DefineVideoStream
    """
    tagId = 61

    streamId: int
    frameNum: int
    videoData: bytes

    def __init__(self, streamId: int, frameNum: int, videoData: bytes) -> None:
        self.streamId = streamId
        self.frameNum = frameNum
        self.videoData = videoData


    @staticmethod
    def read(stream: SWFInputStream) -> Tag:
        streamId = stream.readUI16()
        frameNum = stream.readUI16()
        videoData = stream.read(stream.available())
        return VideoFrameTag(streamId, frameNum, videoData)


    def write(self, stream: SWFOutputStream) -> None:
        stream.writeUI16(self.streamId)
        stream.writeUI16(self.frameNum)
        stream.write(self.videoData)