from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("NotFoundError", "MenuItemNotFoundError")

from .base import RiftError

if TYPE_CHECKING:
    from typing import ClassVar


class NotFoundError(RiftError):
    model: ClassVar[str]

    def __init_subclass__(cls, model: str) -> None:
        cls.model = model


class MenuItemNotFoundError(NotFoundError, model="menu item"):
    ...
