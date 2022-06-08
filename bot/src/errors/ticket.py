from __future__ import annotations

from typing import TYPE_CHECKING

from .. import embeds
from .base import RiftError

__all__ = ("TicketConfigNoDefaultError",)

if TYPE_CHECKING:
    import quarrel


class TicketConfigNoDefaultError(RiftError):
    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.ticket_config_no_default_error(interaction)
