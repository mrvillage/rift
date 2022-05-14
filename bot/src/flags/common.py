from __future__ import annotations

from typing import TYPE_CHECKING, overload

__all__ = ("CommonFlags",)


if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, Optional, TypeVar

    T = TypeVar("T", bound="CommonFlags")


class CommonFlags:
    __slots__ = ("flags",)

    def __init__(self, flags: int = 0) -> None:
        self.flags: int = flags

    @classmethod
    def from_kwargs(cls, **kwargs: bool) -> CommonFlags:
        flags = cls(0)
        for flag, value in kwargs.items():
            setattr(flags, flag, value)
        return flags

    def __add__(self, other: T) -> T:
        return self.__class__(self.flags | other.flags)  # type: ignore

    def __sub__(self, other: T) -> T:
        return self.__class__(self.flags & ~other.flags)  # type: ignore

    def __int__(self) -> int:
        return self.flags

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.flags!r})"


class flag:  # noqa: N801
    def __init__(self, func: Callable[[Any], int]):  # noqa: N801
        self.flag: int = func(None)
        self.__doc__: Optional[str] = func.__doc__

    @overload
    def __get__(self, instance: None, owner: type[T]) -> T:
        ...

    @overload
    def __get__(self, instance: CommonFlags, owner: type[T]) -> bool:
        ...

    def __get__(self, instance: Optional[CommonFlags], owner: type[T]) -> Any:
        return self if instance is None else bool(instance.flags & self.flag)

    def __set__(self, instance: CommonFlags, value: bool) -> None:
        if value:
            instance.flags |= self.flag
        else:
            instance.flags &= ~self.flag
