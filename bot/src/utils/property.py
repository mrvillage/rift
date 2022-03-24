from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, overload

__all__ = ("cached_slotted_property",)

if TYPE_CHECKING:
    from typing import Any, Callable, Optional

    T = TypeVar("T", bound=Any)

R = TypeVar("R", bound="Any")


class cached_slotted_property(property, Generic[R]):  # noqa: N801
    __slots__ = ("name", "func", "__doc__")

    def __init__(self, func: Callable[[Any], R]):  # noqa: N801
        self.name: str = f"_{func.__name__}"
        self.func: Callable[[Any], R] = func
        self.__doc__: Optional[str] = func.__doc__

    @overload
    def __get__(self, instance: None, owner: type[T]) -> T:
        ...

    @overload
    def __get__(self, instance: Any, owner: type[T]) -> R:
        ...

    def __get__(self, instance: Optional[Any], owner: type[T]) -> Any:
        if instance is None:
            return self
        try:
            return getattr(instance, self.name)
        except AttributeError:
            value = self.func(instance)
            setattr(instance, self.name, value)
            return value

    def __set__(self, instance: Any, value: Any) -> None:
        setattr(instance, self.name, value)
