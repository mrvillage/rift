from __future__ import annotations

from typing import Any, Callable, ClassVar, Dict, Optional, Type, TypeVar, overload

__all__ = ("Flags",)

T = TypeVar("T", bound="Flags")
# base class for binary flags
class Flags:
    VALID_FLAGS: ClassVar[Dict[str, Any]]

    __slots__ = "flags"

    def __init__(self, flags: int = 0) -> None:
        self.flags = flags

    @classmethod
    def from_kwargs(cls, **kwargs: bool) -> Flags:
        flags = 0
        for flag, value in kwargs.items():
            if value is not False:
                flags |= cls.VALID_FLAGS[flag]
        return cls(flags)

    @classmethod
    def all(cls) -> Flags:
        flags = 0
        for value in cls.VALID_FLAGS.values():
            flags |= value
        return cls(flags)


# descriptor for flag values
class flag:
    def __init__(self, func: Callable[[Any], int]):
        self.flag = func(None)
        self.__doc__ = func.__doc__

    @overload
    def __get__(self, instance: None, owner: Type[T]) -> T:
        ...

    @overload
    def __get__(self, instance: Flags, owner: Type[T]) -> bool:
        ...

    def __get__(self, instance: Optional[Flags], owner: Type[T]) -> Any:
        if instance is None:
            return self
        return bool(instance.flags & self.flag)

    def __set__(self, instance: Flags, value: bool) -> None:
        if value:
            instance.flags |= self.flag
        else:
            instance.flags &= ~self.flag
