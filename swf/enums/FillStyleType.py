from __future__ import annotations
import enum

class FillStyleType(enum.IntEnum):
    SOLID = 0x00
    LINEAR_GRADIENT = 0x10
    RADIAL_GRADIENT = 0x12
    FOCAL_GRADIENT = 0x13
    REPEATING_BITMAP = 0x40
    CLIPPED_BITMAP = 0x41
    NON_SMOOTHED_REPEATING_BITMAP = 0x42
    NON_SMOOTHED_CLIPPED_BITMAP = 0x43