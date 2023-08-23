from __future__ import annotations
from typing import Any
import os

class Debugging:
    if __debug__:
        try:
            level = int(os.environ.get("PYSWF_DEBUG", 0))
        except ValueError:
            level = 0
    else:
        level = 0

    @staticmethod
    def enableStreamVerbose() -> bool:
        return Debugging.level >= 4
    
    @staticmethod
    def enableTagCounter() -> bool:
        return Debugging.level >= 2
    
    @staticmethod
    def printVerbose(*args: Any, **kwargs: Any) -> None:
        if Debugging.level >= 1:
            print(*args, **kwargs)

    @staticmethod
    def showNotImplemented() -> bool:
        return Debugging.level >= 1
    
    @staticmethod
    def enableRawTag() -> bool:
        return Debugging.level >= 2