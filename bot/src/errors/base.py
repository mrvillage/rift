from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import embeds

__all__ = ("RiftError",)

if TYPE_CHECKING:
    from quarrel import Missing


class RiftError(Exception):
    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.fatal_error(interaction.user)

    def build_grid(self, interaction: quarrel.Interaction) -> Missing[quarrel.Grid]:
        return quarrel.MISSING
