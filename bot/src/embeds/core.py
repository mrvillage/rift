from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import strings, utils

__all__ = (
    "command_is_guild_only_error",
    "fatal_error",
    "missing_discord_permissions_error",
)

if TYPE_CHECKING:
    from ..types.quarrel import MemberOrUser


def command_is_guild_only_error(user: MemberOrUser) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        description=strings.COMMAND_IS_GUILD_ONLY,
        color=quarrel.Color.RED,
    )


def fatal_error(user: MemberOrUser) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        description=strings.FATAL_ERROR,
        color=quarrel.Color.RED,
    )


def missing_discord_permissions_error(
    user: MemberOrUser, permissions: dict[str, bool]
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        description=strings.missing_discord_permissions(permissions),
        color=quarrel.Color.RED,
    )
