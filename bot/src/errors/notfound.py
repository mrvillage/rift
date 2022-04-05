from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = (
    "NotFoundError",
    "AllianceNotFoundError",
    "MenuItemNotFoundError",
    "NationNotFoundError",
)

from .base import RiftError

if TYPE_CHECKING:
    from typing import ClassVar


class NotFoundError(RiftError):
    name: ClassVar[str]

    def __init_subclass__(cls, name: str) -> None:
        # sourcery skip: instance-method-first-arg-name
        cls.name = name


class AllianceNotFoundError(NotFoundError, name="alliance"):
    ...


class MenuItemNotFoundError(NotFoundError, name="menu item"):
    ...


class NationNotFoundError(NotFoundError, name="nation"):
    ...
