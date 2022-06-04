from __future__ import annotations

from typing import TYPE_CHECKING

from .. import embeds
from .base import RiftError

__all__ = (
    "NotFoundError",
    "AllianceNotFoundError",
    "ConditionNotFoundError",
    "MenuItemNotFoundError",
    "MenuNotFoundError",
    "NationNotFoundError",
    "NationOrAllianceNotFoundError",
)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    import quarrel


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

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.not_found_error(interaction, self.name, self.value, self.infer)


class AllianceNotFoundError(NotFoundError, name="alliance", infer=True):
    ...


class ConditionNotFoundError(NotFoundError, name="condition", infer=True):
    ...


class MenuItemNotFoundError(NotFoundError, name="menu item"):
    ...


class MenuNotFoundError(NotFoundError, name="menu"):
    ...


class NationNotFoundError(NotFoundError, name="nation", infer=True):
    ...


class NationOrAllianceNotFoundError(NotFoundError, name="nation or alliance"):
    ...
