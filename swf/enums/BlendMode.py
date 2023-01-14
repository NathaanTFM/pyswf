from __future__ import annotations
import enum

class BlendMode(enum.IntEnum):
    NORMAL_0 = 0
    NORMAL_1 = 1
    LAYER = 2
    MULTIPLY = 3
    SCREEN = 4
    LIGHTEN = 5
    DARKEN = 6
    DIFFERENCE = 7
    ADD = 8
    SUBTRACT = 9
    INVERT = 10
    ALPHA = 11
    ERASE = 12
    OVERLAY = 13
    HARDLIGHT = 14