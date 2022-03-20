from __future__ import annotations

import quarrel

from .. import strings, utils

__all__ = ("command_is_guild_only_error",)


def command_is_guild_only_error(user: quarrel.User | quarrel.Member) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        description=strings.COMMAND_IS_GUILD_ONLY,
        color=quarrel.Color.RED,
    )
