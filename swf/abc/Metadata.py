from __future__ import annotations
class MetadataItem:
    key: str | None
    value: str | None

    def __init__(self, key: str | None, value: str | None) -> None:
        self.key = key
        self.value = value


class Metadata:
    name: str
    items: list[MetadataItem]

    def __init__(self, name: str) -> None:
        self.name = name 
        self.items = []