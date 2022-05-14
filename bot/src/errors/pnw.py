from __future__ import annotations

from typing import TYPE_CHECKING

from .. import embeds, models
from .base import RiftError

__all__ = ("NationNotInAllianceError",)

if TYPE_CHECKING:
    import quarrel


class NationNotInAllianceError(RiftError):
    def __init__(self, nation: models.Nation) -> None:
        self.nation: models.Nation = nation

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.nation_not_in_alliance_error(
            interaction,
            self.nation,
        )
