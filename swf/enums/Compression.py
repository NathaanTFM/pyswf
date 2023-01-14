from __future__ import annotations
import enum

class Compression(enum.IntEnum):
    NONE = 70
    ZLIB = 67
    LZMA = 90