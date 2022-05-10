from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .base import RiftError

__all__ = (
    "NotFoundError",
    "AllianceNotFoundError",
    "MenuItemNotFoundError",
    "NationNotFoundError",
)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional


class NotFoundError(RiftError):
    name: ClassVar[str]
    infer: bool

    def __init_subclass__(cls, name: str, infer: bool = False) -> None:
        # sourcery skip: instance-method-first-arg-name
        cls.name = name
        cls.infer = infer

    def __init__(
        self, interaction: quarrel.Interaction, value: Optional[Any] = None
    ) -> None:
        self.interaction: quarrel.Interaction = interaction
        self.value: Optional[Any] = value


class AllianceNotFoundError(NotFoundError, name="alliance", infer=True):
    ...


class MenuItemNotFoundError(NotFoundError, name="menu item"):
    ...


class NationNotFoundError(NotFoundError, name="nation", infer=True):
    ...
