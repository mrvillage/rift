from __future__ import annotations

from typing import TYPE_CHECKING

from .. import embeds
from .base import RiftError

__all__ = ("GuildOnlyError", "MissingDiscordPermissionsError")

if TYPE_CHECKING:
    import quarrel


class GuildOnlyError(RiftError):
    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.command_is_guild_only_error(interaction)


class MissingDiscordPermissionsError(RiftError):
    def __init__(self, permissions: dict[str, bool]) -> None:
        self.permissions: dict[str, bool] = permissions

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.missing_discord_permissions_error(interaction, self.permissions)
