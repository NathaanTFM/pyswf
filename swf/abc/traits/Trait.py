from __future__ import annotations
from typing import ClassVar
from swf.abc.Metadata import Metadata
from swf.abc.multinames.QName import QName


class Trait:
    kind: ClassVar[int]

    name: QName
    metadata: list[Metadata] | None

    def __init__(self, name: QName) -> None:
        self.name = name
        self.metadata = None