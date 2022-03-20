from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import errors

__all__ = ("guild_only",)

if TYPE_CHECKING:
    from typing import Any

    from ..commands.common import CommonSlashCommand


@quarrel.check(after_options=False)
async def guild_only(command: CommonSlashCommand[Any]) -> bool:
    if command.interaction.guild_id is quarrel.MISSING:
        raise errors.GuildOnlyError()
    return True
