from __future__ import annotations

from typing import Any, Callable, Optional, Type, TypeVar, overload

__all__ = ("Flags",)

T = TypeVar("T", bound="Flags")


class Flags:
    __slots__ = ("flags",)

    def __init__(self, flags: int = 0) -> None:
        self.flags: int = flags

    @classmethod
    def from_kwargs(cls, **kwargs: bool) -> Flags:
        flags = cls(0)
        for flag, value in kwargs.items():
            setattr(flags, flag, value)
        return flags

    def __add__(self, other: T) -> T:
        return self.__class__(self.flags | other.flags)  # type: ignore

    def __sub__(self, other: T) -> T:
        return self.__class__(self.flags & ~other.flags)  # type: ignore


class flag:
    def __init__(self, func: Callable[[Any], int]):
        self.flag: int = func(None)
        self.__doc__: Optional[str] = func.__doc__

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
