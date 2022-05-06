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
    from typing import ClassVar, Optional

    from ..commands.common import CommonCommand


class NotFoundError(RiftError):
    name: ClassVar[str]
    infer: bool

    def __init_subclass__(cls, name: str, infer: bool = False) -> None:
        # sourcery skip: instance-method-first-arg-name
        cls.name = name
        cls.infer = infer

    def __init__(self, command: CommonCommand, value: Optional[str] = None) -> None:
        self.command: CommonCommand = command
        self.value: Optional[str] = value


class AllianceNotFoundError(NotFoundError, name="alliance", infer=True):
    ...


class MenuItemNotFoundError(NotFoundError, name="menu item"):
    ...


class NationNotFoundError(NotFoundError, name="nation", infer=True):
    ...
