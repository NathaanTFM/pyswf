from __future__ import annotations
from typing import Any
import os

class Debugging:
    if __debug__:
        try:
            flag = int(os.environ.get("PYSWF_DEBUG", 0))
        except ValueError:
            flag = 0
    else:
        flag = 0

    @staticmethod
    def enableStreamVerbose() -> bool:
        return Debugging.flag >= 2
    
    @staticmethod
    def enableTagCounter() -> bool:
        return Debugging.flag >= 1
    
    @staticmethod
    def printVerbose(*args: Any, **kwargs: Any) -> None:
        if Debugging.flag >= 1:
            print(*args, **kwargs)

    @staticmethod
    def showNotImplemented() -> bool:
        return Debugging.flag >= 1
    
    @staticmethod
    def enableRawTag() -> bool:
        return Debugging.flag >= 1