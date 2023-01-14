from __future__ import annotations
from swf.tags.Tag import Tag
from swf.tags.EndTag import EndTag
from swf.tags.ShowFrameTag import ShowFrameTag
from swf.tags.DefineShapeTag import DefineShapeTag
from swf.tags.PlaceObjectTag import PlaceObjectTag
from swf.tags.RemoveObjectTag import RemoveObjectTag
from swf.tags.DefineBitsTag import DefineBitsTag
from swf.tags.DefineButtonTag import DefineButtonTag
from swf.tags.JPEGTablesTag import JPEGTablesTag
from swf.tags.SetBackgroundColorTag import SetBackgroundColorTag
from swf.tags.DefineFontTag import DefineFontTag
from swf.tags.DefineTextTag import DefineTextTag
from swf.tags.DoActionTag import DoActionTag
from swf.tags.DefineFontInfoTag import DefineFontInfoTag
from swf.tags.DefineSoundTag import DefineSoundTag
from swf.tags.StartSoundTag import StartSoundTag
from swf.tags.DefineButtonSoundTag import DefineButtonSoundTag
from swf.tags.SoundStreamHeadTag import SoundStreamHeadTag
from swf.tags.SoundStreamBlockTag import SoundStreamBlockTag
from swf.tags.DefineBitsLosslessTag import DefineBitsLosslessTag
from swf.tags.DefineBitsJPEG2Tag import DefineBitsJPEG2Tag
from swf.tags.DefineShape2Tag import DefineShape2Tag
from swf.tags.DefineButtonCxformTag import DefineButtonCxformTag
from swf.tags.ProtectTag import ProtectTag
from swf.tags.PlaceObject2Tag import PlaceObject2Tag
from swf.tags.RemoveObject2Tag import RemoveObject2Tag
from swf.tags.DefineShape3Tag import DefineShape3Tag
from swf.tags.DefineText2Tag import DefineText2Tag
from swf.tags.DefineButton2Tag import DefineButton2Tag
from swf.tags.DefineBitsJPEG3Tag import DefineBitsJPEG3Tag
from swf.tags.DefineBitsLossless2Tag import DefineBitsLossless2Tag
from swf.tags.DefineEditTextTag import DefineEditTextTag
from swf.tags.DefineSpriteTag import DefineSpriteTag
from swf.tags.FrameLabelTag import FrameLabelTag
from swf.tags.SoundStreamHead2Tag import SoundStreamHead2Tag
from swf.tags.DefineMorphShapeTag import DefineMorphShapeTag
from swf.tags.DefineFont2Tag import DefineFont2Tag
from swf.tags.ExportAssetsTag import ExportAssetsTag
from swf.tags.ImportAssetsTag import ImportAssetsTag
from swf.tags.EnableDebuggerTag import EnableDebuggerTag
from swf.tags.DoInitActionTag import DoInitActionTag
from swf.tags.DefineVideoStreamTag import DefineVideoStreamTag
from swf.tags.VideoFrameTag import VideoFrameTag
from swf.tags.DefineFontInfo2Tag import DefineFontInfo2Tag
from swf.tags.EnableDebugger2Tag import EnableDebugger2Tag
from swf.tags.ScriptLimitsTag import ScriptLimitsTag
from swf.tags.SetTabIndexTag import SetTabIndexTag
from swf.tags.FileAttributesTag import FileAttributesTag
from swf.tags.PlaceObject3Tag import PlaceObject3Tag
from swf.tags.ImportAssets2Tag import ImportAssets2Tag
from swf.tags.DefineFontAlignZonesTag import DefineFontAlignZonesTag
from swf.tags.CSMTextSettingsTag import CSMTextSettingsTag
from swf.tags.DefineFont3Tag import DefineFont3Tag
from swf.tags.SymbolClassTag import SymbolClassTag
from swf.tags.MetadataTag import MetadataTag
from swf.tags.DefineScalingGridTag import DefineScalingGridTag
from swf.tags.DoABCTag import DoABCTag
from swf.tags.DefineShape4Tag import DefineShape4Tag
from swf.tags.DefineMorphShape2Tag import DefineMorphShape2Tag
from swf.tags.DefineSceneAndFrameLabelDataTag import DefineSceneAndFrameLabelDataTag
from swf.tags.DefineBinaryDataTag import DefineBinaryDataTag
from swf.tags.DefineFontNameTag import DefineFontNameTag
from swf.tags.StartSound2Tag import StartSound2Tag
from swf.tags.DefineBitsJPEG4Tag import DefineBitsJPEG4Tag
from swf.tags.DefineFont4Tag import DefineFont4Tag
from swf.tags.EnableTelemetryTag import EnableTelemetryTag
from swf.tags.PlaceObject4Tag import PlaceObject4Tag

from swf.tags.ProductInfoTag import ProductInfoTag
from swf.tags.DebugIDTag import DebugIDTag

TagDict: list[type[Tag] | None] = [
    EndTag,                                 # tag 0
    ShowFrameTag,                           # tag 1
    DefineShapeTag,                         # tag 2
    None,
    PlaceObjectTag,                         # tag 4
    RemoveObjectTag,                        # tag 5
    DefineBitsTag,                          # tag 6
    DefineButtonTag,                        # tag 7
    JPEGTablesTag,                          # tag 8
    SetBackgroundColorTag,                  # tag 9
    DefineFontTag,                          # tag 10
    DefineTextTag,                          # tag 11
    DoActionTag,                            # tag 12
    DefineFontInfoTag,                      # tag 13
    DefineSoundTag,                         # tag 14
    StartSoundTag,                          # tag 15
    None,
    DefineButtonSoundTag,                   # tag 17
    SoundStreamHeadTag,                     # tag 18
    SoundStreamBlockTag,                    # tag 19
    DefineBitsLosslessTag,                  # tag 20
    DefineBitsJPEG2Tag,                     # tag 21
    DefineShape2Tag,                        # tag 22
    DefineButtonCxformTag,                  # tag 23
    ProtectTag,                             # tag 24
    None,
    PlaceObject2Tag,                        # tag 26
    None,
    RemoveObject2Tag,                       # tag 28
    None,
    None,
    None,
    DefineShape3Tag,                        # tag 32
    DefineText2Tag,                         # tag 33
    DefineButton2Tag,                       # tag 34
    DefineBitsJPEG3Tag,                     # tag 35
    DefineBitsLossless2Tag,                 # tag 36
    DefineEditTextTag,                      # tag 37
    None,
    DefineSpriteTag,                        # tag 39
    None,
    ProductInfoTag,                         # (undocumented) tag 41
    None,
    FrameLabelTag,                          # tag 43
    None,
    SoundStreamHead2Tag,                    # tag 45
    DefineMorphShapeTag,                    # tag 46
    None,
    DefineFont2Tag,                         # tag 48
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    ExportAssetsTag,                        # tag 56
    ImportAssetsTag,                        # tag 57
    EnableDebuggerTag,                      # tag 58
    DoInitActionTag,                        # tag 59
    DefineVideoStreamTag,                   # tag 60
    VideoFrameTag,                          # tag 61
    DefineFontInfo2Tag,                     # tag 62
    DebugIDTag,                             # (undocumented) tag 63
    EnableDebugger2Tag,                     # tag 64
    ScriptLimitsTag,                        # tag 65
    SetTabIndexTag,                         # tag 66
    None,
    None,
    FileAttributesTag,                      # tag 69
    PlaceObject3Tag,                        # tag 70
    ImportAssets2Tag,                       # tag 71
    None,
    DefineFontAlignZonesTag,                # tag 73
    CSMTextSettingsTag,                     # tag 74
    DefineFont3Tag,                         # tag 75
    SymbolClassTag,                         # tag 76
    MetadataTag,                            # tag 77
    DefineScalingGridTag,                   # tag 78
    None,
    None,
    None,
    DoABCTag,                               # tag 82
    DefineShape4Tag,                        # tag 83
    DefineMorphShape2Tag,                   # tag 84
    None,
    DefineSceneAndFrameLabelDataTag,        # tag 86
    DefineBinaryDataTag,                    # tag 87
    DefineFontNameTag,                      # tag 88
    StartSound2Tag,                         # tag 89
    DefineBitsJPEG4Tag,                     # tag 90
    DefineFont4Tag,                         # tag 91
    None,
    EnableTelemetryTag,                     # tag 93
    PlaceObject4Tag,                        # tag 94
]

__all__ = [
    'Tag',
    
    'EndTag',
    'ShowFrameTag',
    'DefineShapeTag',
    'PlaceObjectTag',
    'RemoveObjectTag',
    'DefineBitsTag',
    'DefineButtonTag',
    'JPEGTablesTag',
    'SetBackgroundColorTag',
    'DefineFontTag',
    'DefineTextTag',
    'DoActionTag',
    'DefineFontInfoTag',
    'DefineSoundTag',
    'StartSoundTag',
    'DefineButtonSoundTag',
    'SoundStreamHeadTag',
    'SoundStreamBlockTag',
    'DefineBitsLosslessTag',
    'DefineBitsJPEG2Tag',
    'DefineShape2Tag',
    'DefineButtonCxformTag',
    'ProtectTag',
    'PlaceObject2Tag',
    'RemoveObject2Tag',
    'DefineShape3Tag',
    'DefineText2Tag',
    'DefineButton2Tag',
    'DefineBitsJPEG3Tag',
    'DefineBitsLossless2Tag',
    'DefineEditTextTag',
    'DefineSpriteTag',
    'FrameLabelTag',
    'SoundStreamHead2Tag',
    'DefineMorphShapeTag',
    'DefineFont2Tag',
    'ExportAssetsTag',
    'ImportAssetsTag',
    'EnableDebuggerTag',
    'DoInitActionTag',
    'DefineVideoStreamTag',
    'VideoFrameTag',
    'DefineFontInfo2Tag',
    'EnableDebugger2Tag',
    'ScriptLimitsTag',
    'SetTabIndexTag',
    'FileAttributesTag',
    'PlaceObject3Tag',
    'ImportAssets2Tag',
    'DefineFontAlignZonesTag',
    'CSMTextSettingsTag',
    'DefineFont3Tag',
    'SymbolClassTag',
    'MetadataTag',
    'DefineScalingGridTag',
    'DoABCTag',
    'DefineShape4Tag',
    'DefineMorphShape2Tag',
    'DefineSceneAndFrameLabelDataTag',
    'DefineBinaryDataTag',
    'DefineFontNameTag',
    'StartSound2Tag',
    'DefineBitsJPEG4Tag',
    'DefineFont4Tag',
    'EnableTelemetryTag',
    'PlaceObject4Tag',

    'ProductInfoTag',
    'DebugIDTag'
]