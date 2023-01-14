from __future__ import annotations
from .Filter import Filter
from .DropShadowFilter import DropShadowFilter
from .BlurFilter import BlurFilter
from .GlowFilter import GlowFilter
from .BevelFilter import BevelFilter
from .GradientGlowFilter import GradientGlowFilter
from .ConvolutionFilter import ConvolutionFilter
from .ColorMatrixFilter import ColorMatrixFilter
from .GradientBevelFilter import GradientBevelFilter

FilterList: list[type[Filter]] = [
    DropShadowFilter,
    BlurFilter,
    GlowFilter,
    BevelFilter,
    GradientGlowFilter,
    ConvolutionFilter,
    ColorMatrixFilter,
    GradientBevelFilter
]