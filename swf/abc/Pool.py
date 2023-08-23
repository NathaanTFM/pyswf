from typing import Generic, Iterator, TypeVar, Hashable
from swf.Debugging import Debugging

T = TypeVar('T')

class Pool(Generic[T]):
    def __init__(self) -> None:
        self.__poolDict: dict[Hashable, int] = {}
        self.__poolList: list[T] = []
        self.__frozen = False


    def _getKey(self, elt: T) -> Hashable:
        raise NotImplementedError


    def getIndex(self, elt: T) -> int | None:
        key = self._getKey(elt)
        if key not in self.__poolDict:
            return None

        return self.__poolDict[key]
    

    def getItem(self, index: int) -> T:
        return self.__poolList[index]
    

    def append(self, elt: T) -> int:
        if self.__frozen:
            raise Exception("Pool is frozen")
        
        index = len(self.__poolList)
        key = self._getKey(elt)

        if key in self.__poolDict:
            Debugging.printVerbose("duplicate element in pool (%r)" % elt)
        else:
            self.__poolDict[key] = index

        self.__poolList.append(elt)
        return index
        

    def clear(self) -> None:
        self.__poolDict.clear()
        self.__poolList.clear()
        self.__frozen = False


    def freeze(self) -> None:
        self.__frozen = True


    def __iter__(self) -> Iterator[T]:
        return self.__poolList.__iter__()
    

    def __len__(self) -> int:
        return len(self.__poolList)
