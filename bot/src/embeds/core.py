from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import consts, strings, utils

__all__ = (
    "command_is_guild_only_error",
    "fatal_error",
    "missing_discord_permissions_error",
)

if TYPE_CHECKING:
    ...


def command_is_guild_only_error(interaction: quarrel.Interaction) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.COMMAND_IS_GUILD_ONLY,
        color=consts.ERROR_EMBED_COLOR,
    )


def fatal_error(interaction: quarrel.Interaction) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.FATAL_ERROR,
        color=consts.ERROR_EMBED_COLOR,
    )


def missing_discord_permissions_error(
    interaction: quarrel.Interaction, permissions: dict[str, bool]
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.missing_discord_permissions(permissions),
        color=consts.ERROR_EMBED_COLOR,
    )
